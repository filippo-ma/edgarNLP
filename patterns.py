
import string


def standardize_item_name(item_name: str):
    item_name_std = item_name.translate(str.maketrans('', '', string.punctuation)).replace('’', '').casefold().strip()

    return item_name_std


ITEM_NAMES_RAW = [
    "Business",
    "Risk Factors",
    "Unresolved Staff Comments",
    "Properties",
    "Legal Proceedings",
    "Mine Safety Disclosures",
    "Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities",
    "Market for Registrant’s Common Equity, Related Shareholder Matters and Issuer Purchases of Equity Securities",
    "Market for Registrant’s Commo",
    "[Reserved]",
    "Selected Financial Data",
    "Management’s Discussion and Analysis of Financial Condition and Results of Operations",
    "Management’s Discussion and Analysis",
    "Quantitative and Qualitative Disclosures About Market Risk",
    "Quantitative and Qualitat",
    "Financial Statements and Supplementary Data",
    "Financial State"
    "Changes in and Disagreements with Accountants on Accounting and Financial Disclosure",
    "Controls and Procedures",
    "Other Information",
    "Disclosure Regarding Foreign Jurisdictions that Prevent Inspections",
    "Directors, Executive Officers and Corporate Governance",
    "Executive Compensation",
    "Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters",
    "Security Ownership of Certain Beneficial Owners and Management and Related Shareholder Matters",
    "Certain Relationships and Related Transactions, and Director Independence",
    "Principal Accounting Fees and Services",
    "Principal Accountant Fees and Services",
    "Exhibit and Financial Statement Schedules",
    "Exhibits and Financial Statement Schedules",
    "Exhibits Financial Statement Schedules",
    "Exhibits and Fina"
    "Form 10-K Summary",
]


ITEM_CODES_CLEAN = [
    'ITEM_1',
    'ITEM_1A',
    'ITEM_1B',
    'ITEM_2',
    'ITEM_3',
    'ITEM_4',
    'ITEM_5',
    'ITEM_6',
    'ITEM_7',
    'ITEM_7A',
    'ITEM_8',
    'ITEM_9',
    'ITEM_9A',
    'ITEM_9B',
    'ITEM_9C',
    'ITEM_10',
    'ITEM_11',
    'ITEM_12',
    'ITEM_13',
    'ITEM_14',
    'ITEM_15',
]

ITEM_NAMES = [standardize_item_name(i) for i in ITEM_NAMES_RAW]

SINGLE_ITEM_PATTERN = r"^item\s+[0-9](..)$|^item\s+[0-9](.)$|^item\s+[0-9]$|^signa"
ITEM_NAME_PATTERN1 = [f"^item\s+[0-9](..)\s+{item.casefold()}\.$|^item\s+[0-9](..)\s+{item.casefold()}$" for item in ITEM_NAMES]
ITEM_NAME_PATTERN2 = [f"^item\s+[0-9](.)\s+{item.casefold()}\.$|^item\s+[0-9](.)\s+{item.casefold()}$" for item in ITEM_NAMES]
ITEM_NAME_PATTERN3 = [f"^item\s+[0-9]\s+{item.casefold()}\.$|^item\s+[0-9]\s+{item.casefold()}$" for item in ITEM_NAMES]

ITEM_PATTERNS = r"|".join(
    ITEM_NAME_PATTERN1
    + ITEM_NAME_PATTERN2
    + ITEM_NAME_PATTERN3
) 



