# Gotham Noir Zsh Ergonomics
[[ -o interactive ]] || return 0
_gotham_steady_cursor() { printf '\e[2 q'; }
autoload -Uz add-zsh-hook && add-zsh-hook precmd _gotham_steady_cursor
export LSCOLORS="Gxfxcxdxbxegedabagacad"
export LS_COLORS="di=1;36:ln=35:so=32:pi=33:ex=31:bd=34;46:cd=34;43:su=30;41:sg=30;46:tw=30;42:ow=30;43"
