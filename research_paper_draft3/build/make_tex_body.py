"""Generate the IEEE LaTeX body from manuscript_source.txt, so both papers carry the same text.

Usage: python -I make_tex_body.py <manuscript_source.txt> <main.tex>

Replaces, in main.tex:
  - the abstract;
  - everything from \\section{Introduction} up to \\section*{Data and Code Availability};
  - the AI declaration paragraphs.
Figures that are drawn in TikZ/pgfplots in the IEEE version are emitted from FIGURES below; the
pipeline figure's TikZ code is kept from the current main.tex. The results table comes from
reruns/results/table_results.tex. Every txt reference must map to a BibTeX key (BIBKEY).
"""
import re
import sys
from pathlib import Path

src, tex_path = Path(sys.argv[1]), Path(sys.argv[2])
txt = src.read_text(encoding='utf-8')
tex = tex_path.read_text(encoding='utf-8')
RESULTS_TEX = src.parent / 'reruns' / 'results' / 'table_results.tex'

# txt reference -> BibTeX key, matched on a phrase of the reference text
BIBKEY = [('World Health Organization, WHO', 'ref01'), ('Atuyambe', 'ref21'), ('Indicator 3.9.1', 'ref22'),
          ('Indicator 11.6.2', 'ref23'), ('D. Okure, J. Ssematimba', 'ref02'), ('Seeing the Air', 'ref03'),
          ('Applying Machine Learning', 'ref04'), ('Lsoto', 'ref05'), ('Scalable Data Pipeline', 'ref_sserunjogi2025'),
          ('Febrian', 'ref06'), ('S. Le et al.', 'ref24'), ('Nagasaki', 'ref07'), ('Seasonal and Regional', 'ref08'),
          ('Multilinear', 'ref09'), ('Niyonzima', 'ref10'), ('Gahungu', 'ref25'), ('Stoddart', 'ref26'),
          ('Pandey', 'ref27'), ('Gupta', 'ref28'), ('AirQo air quality data', 'ref29'),
          ('Data licence and Terms', 'ref_airqo_terms'), ('Alaran', 'ref35'), ('Tukey', 'ref36'), ('BRITS', 'ref11'),
          ('Hochreiter', 'ref12'), ('Pedregosa', 'ref19'), ('SMOTE: Synthetic', 'ref13'), ('SMOTE for Regression', 'ref14'),
          ('Evidently AI', 'ref20'), ('Unified Approach', 'ref15'), ('From Local Explanations', 'ref16'),
          ('Breiman', 'ref17'), ('LightGBM: A Highly', 'ref18'), ('Render, Deploy for Free and Pricing', 'ref_render'),
          ('Vercel Hobby', 'ref32')]
key_of = {}
for n, text in re.findall(r'^@REF \[(\d+)\] (.*)$', txt, flags=re.M):
    hits = [k for phrase, k in BIBKEY if phrase in text]
    assert len(hits) == 1, f'reference [{n}] maps to {hits}: {text[:60]}'
    key_of[int(n)] = hits[0]

body_lines = txt.split('\n')
# section numbers -> labels, figure and table numbers -> labels
SEC_LABEL = {'Related Work': 'sec:related', 'Methodology': 'sec:method', 'Technology Description': 'sec:technology',
             'Developments': 'sec:developments', 'Results': 'sec:results', 'Business Benefits': 'sec:business',
             'Discussion': 'sec:discussion', 'Conclusions and Summary Recommendations': 'sec:conclusions'}
sec_num_to_label, heading_label = {}, {}
for line in body_lines:
    m = re.match(r'^@H([12]) (\d+\.\d+) (.*)$', line) or re.match(r'^@H([12]) (\d+)\. (.*)$', line)
    if m:
        num, title = m.group(2), m.group(3)
        label = SEC_LABEL.get(title, 'sec:' + re.sub(r'[^a-z]+', '-', title.lower()).strip('-'))
        sec_num_to_label[num] = label
        heading_label[line] = (title, label)
FIG_LABEL = {'fig1_pipeline.png': 'fig:pipeline', 'fig2_map.png': 'fig:map', 'fig_eda.png': 'fig:eda',
             'fig_dashboard.png': 'fig:dashboard', 'fig_obspred.png': 'fig:obspred'}
TAB_LABEL = ['tab:models', 'tab:tools', 'tab:results', 'tab:imputation', 'tab:downstream', 'tab:deploy']
fig_num_to_label = {}
for i, line in enumerate(body_lines):
    if line.startswith('@FIG'):
        name = Path(line[5:].split('|')[0].strip()).name
        n = re.match(r'@CAP Figure (\d+):', body_lines[i + 1]).group(1)
        fig_num_to_label[n] = FIG_LABEL[name]


def cite(m):
    numbers = []
    for a, b in re.findall(r'\[(\d+)\](?:-\[(\d+)\])?', m.group(0)):
        numbers += list(range(int(a), int(b) + 1)) if b else [int(a)]
    return '~\\cite{' + ','.join(key_of[n] for n in numbers) + '}'


def conv(s):
    s = s.replace('&', '\\&').replace('%', '\\%')
    s = s.replace(' µg/m³', '~\\ugm{}').replace('µg/m³', '\\ugm{}').replace(' °C', '~\\textdegree{}C').replace('°C', '\\textdegree{}C')
    s = s.replace('R²', '$R^2$')
    s = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', s)
    s = re.sub(r'(\d)-(\d)', r'\1--\2', s)
    s = re.sub(r'(?<![\w$\-])-(\d)', r'$-$\1', s)
    s = re.sub(r'\s?\[\d+\](?:-\[\d+\])?(?:, \[\d+\](?:-\[\d+\])?)*', cite, s)
    s = re.sub(r'Section (\d+(?:\.\d+)?)', lambda m: 'Section~\\ref{' + sec_num_to_label[m.group(1)] + '}', s)
    s = re.sub(r'Figure (\d+)', lambda m: 'Fig.~\\ref{' + fig_num_to_label[m.group(1)] + '}', s)
    s = re.sub(r'Table (\d+)', lambda m: 'Table~\\ref{' + TAB_LABEL[int(m.group(1)) - 1] + '}', s)
    return s


# figure bodies for the IEEE version
pipeline_env = re.search(r'\\begin\{figure\}\[t\]\n\\centering\n(.*?)\\caption\{.*?\}\n\\label\{fig:pipeline\}', tex, re.S)
FIG_BODY = {
    'fig1_pipeline.png': ('figure', pipeline_env.group(1)),
    'fig2_map.png': ('figure*', '\\includegraphics[width=0.82\\textwidth]{map_sensor_network.png}\n'),
    'fig_eda.png': ('figure*', '\\input{figures/fig_eda.tex}\n'),
    'fig_dashboard.png': ('figure', '\\includegraphics[width=\\columnwidth]{dashboard.png}\n'),
    'fig_obspred.png': ('figure*', '\\input{figures/fig_obspred.tex}\n'),
}

out, i, table_count = [], 0, 0
start = next(k for k, l in enumerate(body_lines) if l.startswith('@H1 1. Introduction'))
stop = next(k for k, l in enumerate(body_lines) if l.startswith('@H1 Data and Code Availability'))
lines = body_lines[start:stop]
while i < len(lines):
    line = lines[i]
    if line in heading_label:
        title, label = heading_label[line]
        cmd = '\\section' if line.startswith('@H1') else '\\subsection'
        out.append(f'{cmd}{{{title}}}' + ('' if title == 'Introduction' else f'\\label{{{label}}}') + '\n')
        i += 1
    elif line.startswith('@H2 '):
        out.append('\\subsection*{' + line[4:] + '}\n'); i += 1
    elif line.startswith('@P '):
        out.append(conv(line[3:]) + '\n'); i += 1
    elif line.startswith(('@LN ', '@LB ')):
        env = 'enumerate' if line.startswith('@LN') else 'itemize'
        items = []
        while i < len(lines) and lines[i].startswith(line[:4]):
            items.append('\\item ' + conv(lines[i][4:])); i += 1
        out.append(f'\\begin{{{env}}}\n' + '\n'.join(items) + f'\n\\end{{{env}}}\n')
    elif line.startswith('@FIG '):
        name = Path(line[5:].split('|')[0].strip()).name
        caption = re.sub(r'^@CAP Figure \d+: ', '', lines[i + 1])
        env, body = FIG_BODY[name]
        out.append(f'\\begin{{{env}}}[t]\n\\centering\n{body}\\caption{{{conv(caption)}}}\n\\label{{{FIG_LABEL[name]}}}\n\\end{{{env}}}\n')
        i += 2
    elif line.startswith('@CAP Table'):
        caption = re.sub(r'^@CAP Table \d+: ', '', line)
        label = TAB_LABEL[table_count]; table_count += 1
        i += 1
        cols = int(lines[i].split()[1]); i += 1
        rows = []
        while i < len(lines) and lines[i].startswith('@TR '):
            rows.append(lines[i][4:].split('|')); i += 1
        assert lines[i].startswith('@ENDTABLE'); i += 1
        if label == 'tab:results':
            out.append('\\begin{table*}[t]\n\\caption{' + conv(caption) + '}\n\\label{tab:results}\n\\centering\n\\scriptsize\n'
                       '\\setlength{\\tabcolsep}{3pt}\n' + RESULTS_TEX.read_text() + '\\end{table*}\n')
            continue
        wide = cols >= 6
        env = 'table*' if wide else 'table'
        width = '\\textwidth' if wide else '\\columnwidth'
        spec = 'l' * cols if wide else ('>{\\raggedright\\arraybackslash}X' * cols)
        head = ' & '.join(conv(c) for c in rows[0]) + ' \\\\'
        body = '\n'.join(' & '.join(conv(c) for c in (r + [''] * cols)[:cols]) + ' \\\\' for r in rows[1:])
        tab = (f'\\begin{{tabular}}{{{spec}}}' if wide else f'\\begin{{tabularx}}{{{width}}}{{{spec}}}')
        end = '\\end{tabular}' if wide else '\\end{tabularx}'
        out.append(f'\\begin{{{env}}}[t]\n\\caption{{{conv(caption)}}}\n\\label{{{label}}}\n\\centering\n\\footnotesize\n'
                   f'{tab}\n\\toprule\n{head}\n\\midrule\n{body}\n\\bottomrule\n{end}\n\\end{{{env}}}\n')
    else:
        i += 1
new_body = '\n'.join(out) + '\n'

a = tex.index('\\section{Introduction}')
b = tex.index('\\section*{Data and Code Availability}')
tex = tex[:a] + new_body + tex[b:]

# abstract (PM2.5 and PM10 with subscripts, as before)
abstract = re.search(r'^@ABS Abstract: (.*)$', txt, flags=re.M).group(1)
abstract = conv(abstract).replace('PM2.5', 'PM\\textsubscript{2.5}').replace('PM10', 'PM\\textsubscript{10}')
a = tex.index('\\begin{abstract}') + len('\\begin{abstract}')
b = tex.index('\\end{abstract}')
tex = tex[:a] + '\n' + abstract + '\n' + tex[b:]

# data and code availability, and the AI declaration, from the txt
avail = re.search(r'^@H1 Data and Code Availability\n@P (.*)$', txt, flags=re.M).group(1)
a = tex.index('\\section*{Data and Code Availability}')
b = tex.index('\\section*{Acknowledgment}')
named = ("AirQo data are available from AirQo under CC BY 4.0~\\cite{ref29}; the code and outputs are at "
         "\\url{https://github.com/coleRodneyMigisha/airqo_cole_charis_assgnmnt}.")
tex = tex[:a] + '\\section*{Data and Code Availability}\n\n\\ifblind ' + conv(avail) + '\\else ' + named + '\\fi\n\n' + tex[b:]
decl = [l[3:] for l in txt.split('\n') if l.startswith('@N ')]
a = tex.index('\\section*{Declaration of use')
a = tex.index('\n', a) + 1
b = tex.index('\\bibliographystyle')
first = decl[0].replace('"Hourly PM2.5 Prediction from Sparse Low-Cost Sensor Records in Ugandan Cities"', "``\\papertitle''")
tex = tex[:a] + '\n' + conv(first) + '\n\n' + conv(decl[1]) + '\n\n' + tex[b:]

tex_path.write_text(tex, encoding='utf-8')
print(f'wrote {tex_path}: {len(out)} blocks, {table_count} tables')
