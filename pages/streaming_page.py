class StreamingPage:
    """
    This class knows HOW to interact with the StreamDemo page:
    which selectors to use, which button to click, etc.

    Test files never touch selectors directly — they only call
    methods on this class. If the page's HTML changes, we only
    fix it here, in one place.
    """

    def __init__(self, page):
        self.page = page

    def set_progress(self, show_id: int, value: int):
        self.page.fill(f'[data-testid="progress-input-{show_id}"]', str(value))
        self.page.click(f'[data-testid="set-progress-btn-{show_id}"]')

    def get_progress_label(self, show_id: int) -> str:
        return self.page.locator(f'[data-testid="progress-label-{show_id}"]').inner_text()

    def is_in_continue_watching(self, show_id: int) -> bool:
        row = self.page.locator('[data-testid="continue-watching-row"]')
        card = row.locator(f'[data-testid="show-card-{show_id}"]')
        return card.count() > 0

    def set_premium(self, checked: bool):
        checkbox = self.page.locator('[data-testid="premium-toggle"]')
        if checked:
            checkbox.check()
        else:
            checkbox.uncheck()

    def set_storage_available(self, checked: bool):
        checkbox = self.page.locator('[data-testid="storage-toggle"]')
        if checked:
            checkbox.check()
        else:
            checkbox.uncheck()

    def is_download_enabled(self, show_id: int) -> bool:
        button = self.page.locator(f'[data-testid="download-btn-{show_id}"]')
        return button.is_enabled()

    def search(self, query: str):
        self.page.fill('[data-testid="search-input"]', query)

    def get_all_show_titles(self) -> list:
        cards = self.page.locator('[data-testid="all-shows-row"] .card h3')
        return cards.all_inner_texts()

    def is_no_results_message_visible(self) -> bool:
        return self.page.locator('[data-testid="no-results-message"]').is_visible()