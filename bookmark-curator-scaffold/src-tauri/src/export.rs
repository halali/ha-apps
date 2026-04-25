//! Export categorised bookmarks as a Netscape Bookmark File (the format every
//! browser understands as "Import bookmarks from HTML").

use std::collections::BTreeMap;
use std::path::Path;

use crate::ai::CategorizationOutput;
use crate::error::AppResult;

/// Write `items` to `path` as a Netscape bookmarks HTML file.
pub fn write_html(path: &Path, items: &[CategorizationOutput]) -> AppResult<()> {
    let html = render_html(items);
    std::fs::write(path, html)?;
    Ok(())
}

fn render_html(items: &[CategorizationOutput]) -> String {
    let tree = build_tree(items);
    let mut out = String::new();
    out.push_str(
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>\n\
         <META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html; charset=UTF-8\">\n\
         <TITLE>Bookmarks</TITLE>\n\
         <H1>Bookmarks</H1>\n\
         <DL><p>\n",
    );
    render_node(&tree, 1, &mut out);
    out.push_str("</DL><p>\n");
    out
}

#[derive(Default)]
struct Node {
    /// Subfolder name → child node.
    children: BTreeMap<String, Node>,
    /// Bookmarks living directly in this folder.
    leaves: Vec<Leaf>,
}

struct Leaf {
    title: String,
    url: String,
}

fn build_tree(items: &[CategorizationOutput]) -> Node {
    let mut root = Node::default();
    for it in items {
        let segments: Vec<&str> = it
            .category
            .split('/')
            .map(str::trim)
            .filter(|s| !s.is_empty())
            .collect();
        let mut cursor = &mut root;
        for seg in &segments {
            cursor = cursor
                .children
                .entry((*seg).to_string())
                .or_default();
        }
        cursor.leaves.push(Leaf {
            title: it.title.clone(),
            url: it.url.clone(),
        });
    }
    root
}

fn render_node(node: &Node, depth: usize, out: &mut String) {
    let indent = "    ".repeat(depth);
    for (name, child) in &node.children {
        out.push_str(&format!(
            "{indent}<DT><H3>{name}</H3>\n{indent}<DL><p>\n",
            name = html_escape::encode_safe(name),
            indent = indent,
        ));
        render_node(child, depth + 1, out);
        out.push_str(&format!("{indent}</DL><p>\n", indent = indent));
    }
    for leaf in &node.leaves {
        out.push_str(&format!(
            "{indent}<DT><A HREF=\"{href}\">{title}</A>\n",
            href = html_escape::encode_double_quoted_attribute(&leaf.url),
            title = html_escape::encode_safe(&leaf.title),
            indent = indent,
        ));
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn renders_nested_folders() {
        let items = vec![
            CategorizationOutput {
                url: "https://docs.rs/tokio".into(),
                title: "tokio docs".into(),
                domain: "docs.rs".into(),
                category: "Dev/Rust".into(),
            },
            CategorizationOutput {
                url: "https://news.ycombinator.com".into(),
                title: "HN".into(),
                domain: "news.ycombinator.com".into(),
                category: "News".into(),
            },
        ];
        let html = render_html(&items);
        assert!(html.contains("<H3>Dev</H3>"));
        assert!(html.contains("<H3>Rust</H3>"));
        assert!(html.contains("<H3>News</H3>"));
        assert!(html.contains("https://docs.rs/tokio"));
    }
}
