"""
Home of all importers. 

Importers are bulk operators. I.e. they  read yaml or csv data and 
put them into the database in bulks. This is necessary to get bank 
data, as well as the account structure easily into the database, 
without having to set up everything by hand or one by one.
"""
import arrow
import csv
import logging
import yaml

from kescher.database import get_db
from kescher.models import JournalEntry, Account, Document
from pathlib import Path
from pdfminer.high_level import extract_text
from peewee import DoesNotExist
from tqdm import tqdm


class Importer:
    """
    Importer base class creates the logger instance and the import_date.
    """

    def __init__(self):
        """
        Creates an import date, s.t. all imports of one importer class instance
        have the same date, and therefore can be identified easily in the db.

        Furthermore the logger instance is created.
        """
        self.import_date = arrow.now()
        self.logger = logging.getLogger("kescher.importer." + self.__class__.__name__)


class CsvImporter(Importer):
    def __init__(self, csv_file, delimiter=";", quotechar='"'):
        """
        Must be given a csv file handler (and optionally delimiter and quotechar).
        Creates the csvreader instance to be used when importing.
        """
        self.reader = csv.reader(csv_file, delimiter=";", quotechar='"')
        super().__init__()

    def __call__(self):
        """
        To create a consistent api, all importers are callable.
        """
        self.import_rows()

    def import_rows(self):
        """
        This functions reads all rows and creates temp objects in a list,
        after all lines were read sucessfully, the objects are saved.
        """
        n_rows = 0
        with get_db().atomic() as db:
            for row in tqdm(self.reader):
                self.logger.debug("Creating: " + ", ".join(row))
                JournalEntry.create(
                    date=arrow.get(row[0], "D.M.YYYY").datetime,
                    sender=row[1],
                    receiver=row[2],
                    description=row[3],
                    value=row[4],
                    balance=row[5],
                    imported_at=self.import_date.datetime,
                )
                n_rows += 1
            db.commit()
        self.logger.info(f"Imported {n_rows} entries.")


class AccountImporter(Importer):
    """
    The AccountImporter is a helper to set up your accounts (Kontenrahmen).
    As this can easily done in a yaml file. This yaml file is then loaded 
    into the AccountImporter which will automagically create all accounts
    accordingly.
    """

    def __init__(self, account_file):
        """
        Must be given the account file. Database connection is already established
        at this point, as the parents are referenced accross functions, and we 
        need an established connection to allow this.
        """
        self.account_file = account_file
        self.n_accounts = 0
        super().__init__()
        self.db = get_db().connection()

    def __call__(self):
        """
        To create a consistent api, all importers are callable.
        """
        self.import_accounts()

    def import_accounts(self):
        """
        This wrapper function is to to be called from external
        functions or __call__(). After importing the accounts
        it deletes the class instance and closes the db connection,
        to ensure the db connection is not left open, and then not run again.
        """
        data = yaml.safe_load(self.account_file)
        self._iterate_accounts(data)
        self.logger.info(f"Imported {self.n_accounts} accounts.")
        self.db.close()
        del self

    def _iterate_accounts(self, data, parent=None):
        """
        Iterates over the data (tree) recursively.
        """
        self.logger.debug(f"Iterate accounts with parent {parent}")
        if isinstance(data, list):
            self._create_accounts(data, parent)
            return
        elif isinstance(data, dict):
            for account, children in data.items():
                new_parent = Account(name=account, parent=parent)
                new_parent.save()
                self.n_accounts += 1
                self.logger.debug(
                    f"Created parent {new_parent}. Now creating {children}."
                )
                self._iterate_accounts(children, new_parent)
        else:
            raise TypeError("accounts must be in list or dict")

    def _create_accounts(self, accounts, parent=None):
        """
        Creates all accounts in list, if they are are string, or calls
        _iterate_accounts() again, if they are dict.
        """
        for account in accounts:
            if isinstance(account, str):
                Account.create(name=account, parent=parent)
                self.n_accounts += 1
            elif isinstance(account, dict):
                self._iterate_accounts(account, parent)
            else:
                self.logger.debug(f"account: {account} is {type(account)}")
                raise TypeError("accounts to be created must be str")


class DocumentImporter(Importer):
    """
    The DocumentImporter assists for bulk importing documents.
    """

    EXTENSION = "*.pdf"

    def __init__(self, path):
        self.n_new_documents = 0
        if not isinstance(path, Path):
            path = Path(path)
        self.path = path
        super().__init__()

    def __call__(self):
        self.import_documents()

    def import_documents(self):
        with get_db() as db:
            for doc_path in self.path.glob(self.EXTENSION):
                exists = True
                doc_hash = Document.make_hash(doc_path)
                self.logger.debug(f"Importing {doc_path} ({doc_hash}).")

                try:
                    doc_db = Document.get(Document.path == str(doc_path))
                except DoesNotExist:
                    exists = False

                if not exists:
                    self.logger.debug(f"{doc_path} not found in db. Importing...")
                    doc_content = extract_text(doc_path)
                    Document.create(content=doc_content, hash=doc_hash, path=doc_path)
                    self.n_new_documents += 1
                else:
                    self.logger.debug(
                        f"Checking hash of existing document {doc_path} ..."
                    )
                    if not doc_db.hash == doc_hash:
                        self.logger.warning(
                            f"Hashes of existing and to-be-imported {doc_path} don't match!"
                        )
                    else:
                        self.logger.debug(
                            f"Hash {doc_hash} of doc to be imported matches hash in db."
                        )
        self.logger.info(f"Imported {self.n_new_documents} new documents.")
