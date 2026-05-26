<div align="center">
<img src="assets/mychatarchive-book-logo.png" alt="MyChatArchive" width="200">
</div>

# hermes-mychatarchive

Standalone Hermes memory provider plugin for [MyChatArchive](https://github.com/1ch1n/mychatarchive).

Built for cross-model chat archive memory. Gives Hermes Agent persistent
recall across sessions by searching your local MyChatArchive database
containing imported conversations from ChatGPT, Claude, Cursor, Grok,
and other platforms.

## Why this exists

Most AI memory systems start from scratch each session. But if you have been
using ChatGPT, Claude, Cursor, and Grok for years, you already have tens of
thousands of messages worth of context sitting in exports and logs. This plugin
makes that history searchable by meaning, not just by keyword, and injects it
into Hermes Agent as persistent memory. It is local-first (SQLite + vector
embeddings on your machine or NAS), multi-model (works across any platform
MyChatArchive can import from), and read-heavy by design: your archive is the
source of truth, and Hermes queries it for context via semantic search, keyword
search, and thread summary retrieval. The write path is narrow and explicit
(captured thoughts only), so your archive stays clean.

## Quick start

```bash
# Install the plugin (pulls mychatarchive as a dependency)
pip install git+https://github.com/1ch1n/hermes-mychatarchive

# Register with Hermes
hermes-mychatarchive-install

# Activate
hermes memory setup   # select "mychatarchive"
```

If you don't have an archive yet:

```bash
mychatarchive sync    # import conversations from ChatGPT, Claude, etc.
mychatarchive embed   # generate vector embeddings
```

## Config reference

Config is stored at `$HERMES_HOME/mychatarchive.json`.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `db_path` | string | `~/.mychatarchive/archive.db` | Path to the MCA SQLite database. |
| `recall_mode` | string | `hybrid` | Memory integration mode: `hybrid` (auto-injection + tools), `context` (auto-injection only), `tools` (tools only). |
| `prefetch_limit` | int | `5` | Max chunks auto-injected into context per turn. |

Example `mychatarchive.json`:

```json
{
  "db_path": "~/.mychatarchive/archive.db",
  "recall_mode": "hybrid",
  "prefetch_limit": 5
}
```

## Tool reference

### mca_search

Search the archive for past conversations.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | yes | What to search for. |
| `mode` | string | no | `semantic` (default), `keyword`, or `hybrid`. |
| `limit` | int | no | Max results (default: 10). |
| `platform` | string | no | Filter to a platform (chatgpt, anthropic, grok, claude_code, cursor). |
| `group` | string | no | Filter to a named thread group. |
| `hours_back` | int | no | Only search messages from the last N hours. |

### mca_recall

Rich contextual retrieval combining message chunks, thread summaries, and
captured thoughts for a given topic.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `topic` | string | yes | Topic to recall context about. |
| `limit` | int | no | Max items per category (default: 5). |
| `platform` | string | no | Filter to a platform. |
| `group` | string | no | Filter to a named thread group. |

### mca_remember

Capture a thought or insight into the archive for future retrieval.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `content` | string | yes | The thought or fact to remember. |
| `tags` | string | no | Comma-separated tags. |

### mca_provenance

Look up the full source context for a chunk or thought ID returned by
mca_search or mca_recall. Exactly one of `chunk_id` or `thought_id` is
required.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chunk_id` | string | no | A chunk ID from search/recall results. |
| `thought_id` | string | no | A thought ID from search/recall results. |

## Requirements

- Python 3.10+
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) installed
- A populated MyChatArchive database
  (run `mychatarchive sync && mychatarchive embed` to populate)

The plugin validates embedding dimensions at startup. If the current
model produces vectors with a different dimension than those stored in
the archive, initialization fails with a clear error message and
instructions to either re-embed or restore the original model. MCA
defaults to `sentence-transformers/all-MiniLM-L6-v2` (384-dim, cosine).

## License

MIT
