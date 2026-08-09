import { defineConfig } from "quartz"

export default defineConfig({
  configuration: {
    pageTitle: "AMTB Wiki - 淨空老和尚法教維基",
    pageTitleSuffix: " | AMTB Wiki",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "zh-TW",
    baseUrl: "l2yao.github.io/amtb/wiki",
    ignorePatterns: ["private", "templates", ".obsidian", ".git"],
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Noto Sans TC",
        body: "Noto Serif TC",
        code: "JetBrains Mono",
      },
      colors: {
        lightMode: {
          light: "#fafafa",
          lightgray: "#f0f0f0",
          gray: "#999",
          darkgray: "#666",
          dark: "#222",
          secondary: "#2c5282",
          tertiary: "#38a169",
          highlight: "rgba(44, 82, 130, 0.15)",
          textHighlight: "rgba(255, 242, 54, 0.5)",
        },
        darkMode: {
          light: "#1a1a1a",
          lightgray: "#2d2d2d",
          gray: "#888",
          darkgray: "#ccc",
          dark: "#eee",
          secondary: "#63b3ed",
          tertiary: "#68d391",
          highlight: "rgba(99, 179, 237, 0.15)",
          textHighlight: "rgba(179, 170, 2, 0.5)",
        },
      },
    },
  },
  plugins: {
    transformers: [
      { name: "@quartz-community/created-modified-date", options: { defaultDateType: "modified", priority: ["frontmatter", "git", "filesystem"] } },
      { name: "@quartz-community/syntax-highlighting", options: { theme: { light: "github-light", dark: "github-dark" }, keepBackground: false } },
      { name: "@quartz-community/obsidian-flavored-markdown", options: { enableInHtmlEmbed: false, enableCheckbox: true } },
      { name: "@quartz-community/github-flavored-markdown" },
      { name: "@quartz-community/table-of-contents", options: { layout: { position: "right", priority: 30 } } },
      { name: "@quartz-community/crawl-links", options: { markdownLinkResolution: "shortest" } },
      { name: "@quartz-community/description" },
      { name: "@quartz-community/latex", options: { renderEngine: "katex" } },
      { name: "@quartz-community/alias-redirects" },
      { name: "@quartz-community/remove-draft" },
      { name: "@quartz-community/note-properties", options: { includeAll: true, includedProperties: ["type", "category", "topic", "code", "date", "place", "pages", "tags"], excludedProperties: ["raw", "created", "updated"] } },
      { name: "./quartz/plugins/transformers/prefix-internal-links", options: { basePath: "/amtb/wiki" } },
    ],
    filters: [
      { name: "@quartz-community/remove-draft" },
      { name: "@quartz-community/explicit-publish" },
    ],
    emitters: [
      { name: "@quartz-community/content-page" },
      { name: "@quartz-community/folder-page" },
      { name: "@quartz-community/tag-page" },
      { name: "@quartz-community/content-index", options: { enableSiteMap: true, enableRSS: true } },
      { name: "@quartz-community/alias-redirects" },
      { name: "@quartz-community/sitemap" },
      { name: "@quartz-community/robots-txt" },
    ],
  },
  layout: {
    groups: {
      toolbar: { priority: 35, direction: "row", gap: "0.5rem" },
    },
    byPageType: {
      content: {
        positions: {
          beforeBody: ["breadcrumbs", "article-title", "content-meta"],
          left: ["page-title", "darkmode", "search", "reader-mode", "darkmode"],
          right: ["backlinks", "table-of-contents"],
        },
      },
      folder: {
        exclude: ["reader-mode"],
        positions: {
          right: [],
        },
      },
      tag: {
        exclude: ["reader-mode"],
        positions: {
          right: [],
        },
      },
    },
    groups: {
      toolbar: {
        priority: 35,
        direction: "row",
        gap: "0.5rem",
      },
    },
  },
})