"""Page object for OpenSemanticLab's JSON editor forms."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from osw_selenium.config import OSWConfig
from osw_selenium.pages.base import BasePage
from osw_selenium.utils import schema_path_to_name, schema_path_to_property_checkbox_id


class JsonEditorPage(BasePage):
    """Page object for OSL JSON editor forms.

    Manages a stack-based editor level to handle nested inline editors.
    Each nested editor increments the level; saving/cancelling decrements it.
    The current ``editor_id`` (the DOM id of the ``.je-ready`` element at the
    current level) is updated automatically when the level changes.

    Args:
        driver: The Selenium WebDriver instance.
        config: The OSW test configuration.
        default_timeout: Default explicit wait timeout in seconds.
    """

    CREATE_INSTANCE_TAB = (By.ID, "ca-create-instance")
    EDIT_DATA_TAB = (By.ID, "ca-edit-data")
    JE_READY = (By.CSS_SELECTOR, ".je-ready")
    PROPERTIES_BUTTON = (By.CSS_SELECTOR, ".json-editor-btntype-properties")

    def __init__(self, driver: WebDriver, config: OSWConfig, default_timeout: int = 10) -> None:
        super().__init__(driver, config, default_timeout)
        self._editor_level: int = -1
        self._editor_id: str | None = None

    # --- Editor level management ---

    @property
    def editor_level(self) -> int:
        """Current editor nesting level (0-based, -1 means no editor open)."""
        return self._editor_level

    @property
    def editor_id(self) -> str | None:
        """DOM id of the ``.je-ready`` element at the current editor level."""
        return self._editor_id

    def _update_editor_id(self) -> str | None:
        """Fetch the DOM id of the current-level ``.je-ready`` element.

        Returns:
            The DOM id string, or None if level is -1.
        """
        if self._editor_level == -1:
            self._editor_id = None
        else:
            self._editor_id = self.driver.execute_script(
                "return document.querySelectorAll('.je-ready')[arguments[0]].id;",
                self._editor_level,
            )
        return self._editor_id

    def _increment_editor_level(self) -> int:
        """Increment the editor level and update the editor id.

        Returns:
            The new editor level.
        """
        self._editor_level += 1
        self._update_editor_id()
        return self._editor_level

    def _decrement_editor_level(self) -> int:
        """Decrement the editor level and update the editor id.

        Returns:
            The new editor level.
        """
        self._editor_level -= 1
        self._update_editor_id()
        return self._editor_level

    # --- Form navigation ---

    def open_create_instance_form(self, category: str) -> None:
        """Navigate to a category page and open the create-instance editor.

        Args:
            category: The full category name
                (e.g. ``Category:OSW0e7fab2262fb4427ad0fa454bc868a0d``).
        """
        self.navigate_to("/wiki/" + category)
        self._editor_level = -1
        self.add_notification(text="Navigate to the Category and click 'Create Instance'")
        self.enable_cursor()
        self.scroll_and_move(self.CREATE_INSTANCE_TAB)
        self.wait(3)
        self.scroll_and_click(self.CREATE_INSTANCE_TAB)
        self.wait_for_element(self.JE_READY, timeout=5)
        self.scroll_and_move((By.CSS_SELECTOR, ".je-ready .card-title"))
        self._increment_editor_level()

    def open_edit_instance_form(self, title: str) -> None:
        """Navigate to a wiki page and open the edit-data editor.

        Args:
            title: The full page title.
        """
        self.navigate_to("/wiki/" + title)
        self._editor_level = -1
        self.add_notification(text="Navigate to the Item and click 'Edit Data'")
        self.enable_cursor()
        self.scroll_and_move(self.EDIT_DATA_TAB)
        self.wait(3)
        self.scroll_and_click(self.EDIT_DATA_TAB)
        self.wait_for_element(self.JE_READY, timeout=5)
        self.scroll_and_move((By.CSS_SELECTOR, ".je-ready .card-title"))
        self._increment_editor_level()

    # --- Field interaction ---

    def fill_editor_field(self, schemapath: str, value: str) -> None:
        """Fill a field in the current editor by its schema path.

        Args:
            schemapath: Dot-separated path like ``root.label.0.text``.
            value: The value to fill.
        """
        name = schema_path_to_name(schemapath)
        selector = f'#{self._editor_id} [name="{name}"]'
        self.scroll_and_fill((By.CSS_SELECTOR, selector), value)

    def add_additional_property(self, schemapath: str) -> None:
        """Add an additional property by toggling the properties checkbox.

        Args:
            schemapath: Dot-separated path like ``root.orderer``.
        """
        self.add_notification(text="Select the property from the list")
        self.scroll_and_click(self.PROPERTIES_BUTTON)
        checkbox_id = schema_path_to_property_checkbox_id(schemapath)
        self.scroll_and_check((By.ID, checkbox_id))
        self.scroll_and_click(self.PROPERTIES_BUTTON)

    def add_array_element(self, schemapath: str) -> None:
        """Click the add button for an array field.

        Args:
            schemapath: Dot-separated path like ``root.actionees``.
        """
        selector = f'#{self._editor_id} [data-schemapath="{schemapath}"] .json-editor-btn-add'
        self.scroll_and_click((By.CSS_SELECTOR, selector))

    def create_inline(self, schemapath: str) -> None:
        """Open an inline editor for the given field.

        Clicks the inline-edit button and waits for the nested ``.je-ready``
        editor to appear, then increments the editor level.

        Args:
            schemapath: Dot-separated path like ``root.orderer``.
        """
        btn_selector = f'[data-schemapath="{schemapath}"] .inline-edit-btn'
        self.scroll_and_move((By.CSS_SELECTOR, btn_selector))
        self.find_element((By.CSS_SELECTOR, btn_selector)).click()
        # XPath index is 1-based; wait for the next editor level to appear
        next_level_xpath = f'(//*[@class="je-ready"])[{self._editor_level + 2}]'
        self.wait_for_visible((By.XPATH, next_level_xpath), timeout=10)
        self._increment_editor_level()

    def select_autocomplete_result(self, schemapath: str, index: int = 0, input_text: str | None = None) -> None:
        """Type into an autocomplete field and select a result.

        Args:
            schemapath: Dot-separated path for the autocomplete field.
            index: Zero-based index of the autocomplete result to select.
            input_text: Optional text to type to trigger autocomplete.
        """
        field_selector = f'#{self._editor_id} [data-schemapath="{schemapath}"]'
        self.scroll_and_click((By.CSS_SELECTOR, field_selector))
        if input_text is not None:
            self.find_element((By.CSS_SELECTOR, field_selector)).send_keys(input_text)
        self.wait(5)
        result_selector = f'#{self._editor_id} [data-schemapath="{schemapath}"] #autocomplete-result-{index}'
        self.scroll_and_click((By.CSS_SELECTOR, result_selector))
        self.wait(1)

    # --- Save / Cancel ---

    def save_editor(self) -> None:
        """Save the current editor level.

        Collapses the editor, clicks the primary action button in the OOUI
        dialog, handles confirmation modals, and dismisses notifications.
        """
        self.add_notification(text="Save your changes")

        # Collapse the editor by clicking its level-1 card title
        self.find_element((By.CSS_SELECTOR, f"#{self._editor_id} .card-title.level-1")).click()

        # Click the primary action button via XPath (1-based index)
        primary_xpath = (
            f'(//*[@class="je-ready"])[{self._editor_level + 1}]'
            '/ancestor::*[contains(@class,"oo-ui-window-content")]'
            '//*[contains(@class,"oo-ui-processDialog-actions-primary")]'
            '//*[contains(@class,"oo-ui-buttonElement-button")]'
        )
        self.scroll_and_click((By.XPATH, primary_xpath))

        # Handle confirmation dialog if present
        if self.count_visible_elements(".oo-ui-messageDialog-content") > 0:
            ok_button_xpath = (
                '(//*[contains(@class,"oo-ui-messageDialog-content")]//*[@class="oo-ui-buttonElement-button"])[2]'
            )
            self.scroll_and_click((By.XPATH, ok_button_xpath))

        # Wait for the current editor to disappear
        if self._editor_id is None:
            msg = "No editor is open (editor_id is None)."
            raise RuntimeError(msg)
        self.wait_for_invisible((By.ID, self._editor_id), timeout=10)
        self._decrement_editor_level()
        self.wait(1)

        # Dismiss MediaWiki notifications
        self.dismiss_notifications()

    def cancel_editor(self) -> None:
        """Cancel the current editor level without saving."""
        # Click the safe (cancel) action button via XPath
        cancel_xpath = (
            f'(//*[@class="je-ready"])[{self._editor_level + 1}]'
            '/ancestor::*[contains(@class,"oo-ui-window-content")]'
            '//*[contains(@class,"oo-ui-processDialog-actions-safe")]'
            '//*[contains(@class,"oo-ui-buttonElement-button")]'
        )
        self.scroll_and_click((By.XPATH, cancel_xpath))

        # Wait for the current editor to disappear
        if self._editor_id is None:
            msg = "No editor is open (editor_id is None)."
            raise RuntimeError(msg)
        self.wait_for_invisible((By.ID, self._editor_id), timeout=10)
        self._decrement_editor_level()
        self.wait(1)

    # --- Assertions ---

    def assert_field_has_value(self, schemapath: str, expected: str) -> None:
        """Assert that a field's current value matches the expected string.

        Args:
            schemapath: Dot-separated path for the field.
            expected: The expected value.

        Raises:
            AssertionError: If the field value does not match.
        """
        name = schema_path_to_name(schemapath)
        value = self.driver.execute_script(f"return document.querySelector('[name=\"{name}\"]').value")
        if value != expected:
            msg = f"Expected field {schemapath!r} to have value {expected!r}, got {value!r}"
            raise AssertionError(msg)

    def assert_field_not_has_value(self, schemapath: str, not_expected: str) -> None:
        """Assert that a field's current value does NOT match the given string.

        Args:
            schemapath: Dot-separated path for the field.
            not_expected: The value that should not be present.

        Raises:
            AssertionError: If the field value matches.
        """
        name = schema_path_to_name(schemapath)
        value = self.driver.execute_script(f"return document.querySelector('[name=\"{name}\"]').value")
        if value == not_expected:
            msg = f"Expected field {schemapath!r} NOT to have value {not_expected!r}"
            raise AssertionError(msg)
