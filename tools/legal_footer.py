"""Shared legal footer HTML. prefix = relative path to site root ('' or '../../')."""
def legal_footer(prefix=""):
    return (
        '<div class="yk-legal">'
        '<div><strong>YK CROWN, LDA</strong> · NIPC 514037555 · Rua Fontes Pereira de Melo 22B, 2720-233 Amadora, Portugal · '
        '<a href="mailto:info@ykcrown.com">info@ykcrown.com</a> · <a href="tel:+351969058818">+351 969 058 818</a></div>'
        f'<div><a href="{prefix}privacidade.html">Política de Privacidade · Privacy</a> · '
        '<a href="https://www.livroreclamacoes.pt/Inicio/" rel="noopener" target="_blank">Livro de Reclamações</a> · '
        'Resolução alternativa de litígios: <a href="https://www.cniacc.pt" rel="noopener" target="_blank">CNIACC</a> '
        '(<a href="https://www.consumidor.gov.pt" rel="noopener" target="_blank">consumidor.gov.pt</a>)</div>'
        '</div>'
    )
