import asyncio

import gspread_asyncio
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_PATH = "./service_account.json"
LINK_FILENAME = "./sheet_links.txt"
DUMP_FILENAME = "./title_dump.txt"


def load_links() -> list[str]:
    """Read the sheet link file and return a list of urls"""
    with open(LINK_FILENAME, "r") as f:
        return list(filter(None, f.read().split("\n")))


def dump_to_file(data, filename=DUMP_FILENAME) -> None:
    """Dump the data to a file, by default to a 'title_dump.txt' file"""
    with open(filename, "a") as f:
        f.write(data + "\n")


def get_credentials() -> Credentials:
    """Return the service account credentials for the API"""
    service_account_credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_PATH
    )
    scoped_service_account_credentials = service_account_credentials.with_scopes(
        ["https://www.googleapis.com/auth/spreadsheets"]
    )
    return scoped_service_account_credentials


async def run_async(
    urls: list[str],
    async_gspread_client_manager: gspread_asyncio.
    AsyncioGspreadClientManager,
) -> list[str]:
    """Run the Async gspread client and gather a list of strings"""
    print("Authorizing the client manager.")
    async_gspread_client = await async_gspread_client_manager.authorize()
    print("Authorized.")

    async_tasks = [
        await get_spreadsheet_url_async(async_gspread_client, url)
        for url in urls
    ]
    print("Task count:", len(async_tasks))
    return await asyncio.gather(*async_tasks)


async def get_spreadsheet_url_async(
    client: gspread_asyncio.AsyncioGspreadClient, url: str
):
    """Get the spreadsheet URL asynchronously"""
    ss: gspread_asyncio.AsyncioGspreadSpreadsheet = await client.open_by_url(
        url
    )
    title: str = await ss.get_title()
    row = f"{url}, {title}"
    print("Found:", row)
    dump_to_file(data=row)
    return title


async def main():
    urls = load_links()
    async_gspread_client_manager = gspread_asyncio.AsyncioGspreadClientManager(
        get_credentials
    )
    titles = await run_async(urls, async_gspread_client_manager)
    print("Finished.")
    print("Here are the titles found.")
    print(titles)


if __name__ == "__main__":
    asyncio.run(
        main()
    )  # If something doesn't work, add ", debug=True" argument
