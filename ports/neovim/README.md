# Gotham Noir for Neovim

Native Lua + Treesitter + LSP colorscheme supporting Python, TypeScript, Go, Rust, YAML, Terraform (HCL), and Kubernetes manifests.

## Install with lazy.nvim

```lua
{
  "thezaynahmed/gotham-noir",
  config = function(plugin)
    vim.opt.rtp:append(plugin.dir .. "/ports/neovim")
    require("gotham_noir").setup({ variant = "year-one" })
    vim.cmd.colorscheme("gotham-noir-year-one")
  end,
}
```
