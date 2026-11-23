-- Gotham Noir Neovim Colorscheme Plugin
local palettes = require("gotham_noir.palettes")
local M = { variant = "year-one" }

function M.setup(opts)
  opts = opts or {}
  if opts.variant and palettes[opts.variant] then
    M.variant = opts.variant
  end
end

function M.load(variant)
  local key = variant or M.variant or "year-one"
  local p = palettes[key] or palettes["year-one"]
  vim.cmd("highlight clear")
  if vim.fn.exists("syntax_on") == 1 then
    vim.cmd("syntax reset")
  end
  vim.o.termguicolors = true
  vim.o.background = "dark"
  vim.g.colors_name = "gotham-noir-" .. key

  local hi = function(group, spec)
    vim.api.nvim_set_hl(0, group, spec)
  end

  hi("Normal", { fg = p.fg, bg = p.bg })
  hi("NormalFloat", { fg = p.fg, bg = p.elevated })
  hi("FloatBorder", { fg = p.border, bg = p.elevated })
  hi("CursorLine", { bg = p.line_highlight })
  hi("CursorLineNr", { fg = p.accent, bold = true })
  hi("LineNr", { fg = p.gutter })
  hi("Visual", { bg = p.selection })
  hi("StatusLine", { fg = p.fg_strong, bg = p.bg_side })
  hi("VertSplit", { fg = p.border })
  hi("WinSeparator", { fg = p.border })
  hi("Search", { fg = p.accent_fg, bg = p.accent })
  hi("IncSearch", { fg = p.accent_fg, bg = p.blue })

  -- Core Vim & 7-Language Treesitter groups (Python, TS, Go, Rust, YAML, Terraform/HCL)
  hi("Comment", { fg = p.muted, italic = true })
  hi("Keyword", { fg = p.violet })
  hi("Function", { fg = p.blue })
  hi("Type", { fg = p.gold })
  hi("String", { fg = p.emerald })
  hi("Number", { fg = p.amber })
  hi("Boolean", { fg = p.amber })
  hi("Constant", { fg = p.amber })
  hi("Operator", { fg = p.cyan })
  hi("Identifier", { fg = p.fg })
  hi("Special", { fg = p.rose })
  hi("DiagnosticError", { fg = p.crimson })
  hi("DiagnosticWarn", { fg = p.gold })
  hi("DiagnosticInfo", { fg = p.blue })
  hi("DiagnosticHint", { fg = p.cyan })
  hi("DiffAdd", { fg = p.emerald, bg = p.bg_deep })
  hi("DiffChange", { fg = p.gold, bg = p.bg_deep })
  hi("DiffDelete", { fg = p.crimson, bg = p.bg_deep })

  hi("@comment", { fg = p.muted, italic = true })
  hi("@keyword", { fg = p.violet })
  hi("@keyword.import", { fg = p.violet })
  hi("@function", { fg = p.blue })
  hi("@function.call", { fg = p.blue })
  hi("@function.macro", { fg = p.cyan })
  hi("@type", { fg = p.gold })
  hi("@type.builtin", { fg = p.gold })
  hi("@string", { fg = p.emerald })
  hi("@number", { fg = p.amber })
  hi("@boolean", { fg = p.amber })
  hi("@constant", { fg = p.amber })
  hi("@operator", { fg = p.cyan })
  hi("@variable", { fg = p.fg })
  hi("@variable.parameter", { fg = p.amber })
  hi("@variable.builtin", { fg = p.rose })
  hi("@property", { fg = p.cyan })
  hi("@attribute", { fg = p.violet })
  hi("@tag", { fg = p.blue })
  hi("@tag.attribute", { fg = p.cyan })
  hi("@punctuation.delimiter", { fg = p.fg })
  hi("@markup.heading", { fg = p.gold, bold = true })

  for i = 0, 15 do
    vim.g["terminal_color_" .. i] = p.terminal[i + 1]
  end
end

return M
