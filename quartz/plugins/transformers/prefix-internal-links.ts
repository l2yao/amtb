import { defineTransformer } from "quartz/plugins/loader/config-loader"

export const prefixInternalLinks = defineTransformer({
  name: "prefix-internal-links",
  options: {
    basePath: "/amtb/wiki",
  },
  order: 100,
  async transform(ctx, content, { basePath }) {
    if (!basePath) return content

    const { unified } = await import("unified")
    const rehypeParse = (await import("rehype-parse")).default
    const rehypeStringify = (await import("rehype-stringify")).default

    const processor = unified()
      .use(rehypeParse, { fragment: true })
      .use(() => (tree: any) => {
        function visit(node: any) {
          if (node.type === "element" && node.properties?.href) {
            const href = node.properties.href as string
            if (
              href.startsWith("/") &&
              !href.startsWith("//") &&
              !href.startsWith("http://") &&
              !href.startsWith("https://") &&
              !href.startsWith("mailto:") &&
              !href.startsWith("tel:") &&
              !href.startsWith("#")
            ) {
              const [path, hash] = href.split("#")
              node.properties.href = `${basePath}${path}${hash ? `#${hash}` : ""}`
            }
          }
          if (node.children) {
            for (const child of node.children) {
              visit(child)
            }
          }
        }
        visit(tree)
      })
      .use(rehypeStringify)

    return await processor.stringify(await processor.parse(content))
  },
})