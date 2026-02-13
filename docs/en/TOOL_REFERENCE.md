# MCP Server Tool Reference

This document provides a detailed reference for all tools available in the MCP server, organized by category. For usage examples and API details, see the main README or category-specific documentation.

---

## 📦 Compression Tools (5)

### `compress_zip`
Create a ZIP archive from files.

### `extract_zip`
Extract files from a ZIP archive with security checks.

### `compress_tar`
Create a TAR archive (optionally compressed with gzip or bzip2).

### `extract_tar`
Extract files from a TAR archive.

### `list_archive_contents`
List contents of a ZIP or TAR archive without extracting.

---

## 🌐 Web & Network Tools (18)

- `web_search`: DuckDuckGo search
- `fetch_webpage`: Fetch HTML content
- `fetch_webpage_text`: Extract clean text
- `parse_html`: CSS selector parsing
- `download_file`: Download files
- `get_page_title`: Extract page title
- `get_page_links`: Extract all links
- `check_url_status`: HTTP status check
- `get_headers`: HTTP headers
- `validate_url_format`: URL validation
- `parse_url_components`: URL parsing
- `web_search_news`: News search
- `http_request`: Generic HTTP client
- `get_network_info`: Network info
- `dns_lookup`: DNS lookup

---

## 📁 File System Tools (12)

- `read_file`, `write_file`, `append_file`
- `list_directory`, `file_exists`, `get_file_info`
- `search_files`, `create_directory`, `delete_file`, `copy_file`
- `diff_files`, `diff_text`

---

## 📊 Data Processing Tools (15)

- `parse_json`, `format_json`, `json_query`, `csv_to_json`, `json_to_csv`, `parse_csv`, `validate_json_schema`, `flatten_json`, `merge_json`, `xml_to_json`, `parse_yaml`, `yaml_to_json`, `json_to_yaml`, `parse_toml`, `toml_to_json`

---

## 📝 Text Processing Tools (9)

- `count_words`, `extract_emails`, `extract_urls`, `regex_match`, `regex_replace`, `text_summary`, `encode_base64`, `decode_base64`, `calculate_text_similarity`

---

## 💻 System Tools (8)

- `get_system_info`, `get_cpu_info`, `get_memory_info`, `get_disk_info`, `get_env_variable`, `list_env_variables`, `get_current_time`, `get_process_info`

---

## 🛠️ Utility Tools (10)

- `generate_uuid`, `generate_hash`, `timestamp_to_date`, `date_to_timestamp`, `calculate_date_diff`, `format_date`, `calculate_expression`, `generate_random_string`, `generate_password`, `check_password_strength`

---

## 🤖 Subagent AI Orchestration (6)

- `subagent_call`, `subagent_parallel`, `subagent_conditional`, `subagent_config_set`, `subagent_config_get`, `subagent_config_list`

---

For detailed usage, see the main README or category-specific documentation in the docs folder.
