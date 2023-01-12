# John McLevey
# February 24, 2021

import os
import re
import string
from os import walk
import string
import pandas as pd

# def get_markdown_files(directory='generated'):
#     a, _, filenames = next(walk(directory))
#     files = [a + '/' + f for f in filenames if '.md' in f]
#     return files

# def parse_chapter(markdown):
#     with open(markdown, 'r') as f:
#         lines = f.readlines()
#         body = lines[1:]
#         title = lines[0].replace('# <font color="#49699E" size=40>',
#                                  '').replace('</font>', '')
#         title = title.split(':',1) # ,1 means splits on the first occurrence only! :)
#         c_number = title[0]
#         c_string = title[1].strip()
#     return c_number, c_string, body, markdown







#
# NOTHING BELOW HERE IS BEING USED RIGHT NOW,
# BUT I AM LEAVING IT AS IS UNTIL I CAN SAFELY REFACTOR
#


def yell_at_me(task_to_yell_about, how_loud=30, symbol='🙀'):
        """
        Sometimes I like to be yelled at on the command line...
        """
        print(f'\n{symbol*how_loud} {task_to_yell_about}\n')


def dataframe_to_table(df, filename, caption, columns, nrows=5, show=True):
    df.head(nrows).to_latex(f'../tables/{filename}', columns=columns, caption=caption)
    with open(f'../tables/{filename}', 'r', encoding='UTF-8') as infile:
        new_table = []
        for line in infile:
            if r'\begin{table}' in line:
                line = line.replace('\n','') + '[!h]\n'
            new_table.append(line)
    with open(f'../tables/{filename}', 'w', encoding='UTF-8') as outfile:
        for line in new_table:
            outfile.write(line)
    if show is True:
        return df.head(nrows)


def get_title_and_body(markdown):
        with open(markdown, 'r') as f:
                lines = f.readlines()
                title = lines[0].replace('# <font color="#49699E" size=40>','').replace('</font>','')
                title = title.split(':')[0]
                # tons of functions nested here... sorry!
                body = clean_code_cells(swap_table_here_to_tex([l for l in lines[1:]]))
        return title, body

def convert_notebook_to_markdown(notebook):
        """
        Accepts a jupyter notebook, returns a markdown file.
        If the notebook was executed, results will be inline.
        """
        os.system(f'jupyter nbconvert --to markdown {notebook}')

def load_metadata(metadata='meta.md'):
        with open('templates/meta.md', 'r') as f:
                meta = f.readlines()
                title_string_corrected = []
                for line in meta:
                    if line.startswith('title: '):
                        line = line.replace('title: ', 'title: "')
                        line = line.replace('\n','') + '"' + '\n'
                    title_string_corrected.append(line)
                meta = "".join(title_string_corrected)
        return meta


replacements = [
    [r'_', r'\_'],
    [r'α', r'$\alpha$'],
    [r'β', r'$\beta$'],
    [r'γ', r'$\gamma$'],
    [r'δ', r'$\delta$'],
    [r'ϵ', r'$\epsilon$'],
    [r'ε', r'$\epsilon$'],
    [r'ζ', r'$\zeta$'],
    [r'η', r'$\eta$'],
    [r'θ', r'$\theta$'],
    [r'ϑ', r'$\theta$'],
    [r'λ', r'$\lambda$'],
    [r'μ', r'$\mu$'],
    [r'τ', r'$\tau$'],
    [r'ϕ', r'$\phi$'],
    [r'φ', r'$\phi$'],
    [r'χ', r'$\chi$'],
    [r'ψ', r'$\psi$'],
    [r'ω', r'$\omega']
]


def concatenate_meta_chapter(title, body, replacements=[[r'\text{test_prior}', r'\text{test\_prior}'],
                                                       [r'text{another_test}', r'text{another\_test}']], write=True):
    """
    With optional replacements, e.g., escaping characters that trip up LaTeX such as _.
    """
    metadata = load_metadata()
    metadata = metadata.replace('CHAPTER_TITLE', title.replace('\n', ''))
    metadata = '---\n' + metadata + '\n---\n\n'

    if write is True:
        filename = title.replace(' ', '_').translate(str.maketrans(
            '', '', string.punctuation)).replace('\n', '') + '.md'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(metadata)
            for line in body:
                for rep in replacements:
                    line = line.replace(rep[0], rep[1])
                f.write(line)
        return filename
    else:
        return filename



#def concatenate_meta_chapter(title, body, replacements=[[r'_', r'\_'],[r'α',r'$\alpha$'],[r'β',r'$\beta$'],[r'γ',r'$\gamma$'],[r'δ',r'$\delta$'],[r'ϵ',r'$\epsilon$'],[r'ε',r'$\epsilon$'],[r'ζ',r'$\zeta$'],[r'η',r'$\eta$'],[r'θ',r'$\theta$'],[r'ϑ',r'$\theta$'],[r'λ',r'$\lambda$'],[r'μ',r'$\mu$'],[r'τ',r'$\tau$'],[r'ϕ',r'$\phi$'],[r'φ',r'$\phi$'],[r'χ',r'$\chi$'],[r'ψ',r'$\psi$'],[r'ω',r'$\omega]], write=True):
#    """
#    With optional replacements, e.g., escaping characters that trip up LaTeX such as _.
#    """
#    metadata = load_metadata()
#    metadata = metadata.replace('CHAPTER_TITLE', title.replace('\n',''))
#    metadata = '---\n' + metadata + '\n---\n\n'
#
#    if write is True:
#        filename = title.replace(' ','_').translate(str.maketrans('', '', string.punctuation)).replace('\n','') + '.md'
#        with open(filename, 'w', encoding='utf-8') as f:
#            f.write(metadata)
#            for line in body:
#                for rep in replacements:
#                    line = line.replace(rep[0], rep[1])
#                    f.write(line)
#        return filename
#    else:
#        return filename

def markdown_to_pdf(file_to_process, show_figures=True, template='templates/eisvogel.tex', pdf=True):
        pdf_filename = file_to_process.split('.')[0] + '.pdf'
        process_figures(file_to_process, show_figures)
        if pdf is True:
            os.system(f'pandoc --pdf-engine=xelatex --include-in-header templates/listings-code.tex {file_to_process} -o {pdf_filename} --from markdown --template={template} --citeproc --bibliography=templates/refs.bib --listings')

def swap_table_here_to_tex(body):
    stripped = []
    for l in body:
        if '<center><font color="#49699E"><strong>TABLE' in l:
            l = l.replace('<center><font color="#49699E"><strong>TABLE ', r'\input{../tables/')
            l = l.replace(' HERE</strong></font></center>','.tex}')
        stripped.append(l)
    return stripped


def clean_code_cells(body):
    stripped = []
    for l in body:
        if 'dataframe_to_table(' in l:
            l = l.replace('dataframe_to_table(', '').split(',')[0] + '.head()\n'
        stripped.append(l)
    return stripped


def process_figures(file_to_process, show_figures):
        figure_counter = 1
        new_content = []

        with open(file_to_process, 'r') as infile:
                content = infile.readlines()
                for line in content:
                        if '![' in line:
                                caption = f'FIGURE {figure_counter} HERE'
                                line = line.replace('[png]', f'[{caption}]')
                                line = line.replace('[cap]', f'[{caption}]')
                                if '.png' in line:
                                        line = line.replace('.png)', '.pdf)')
                                figure_counter += 1
                        new_content.append(line)

        if show_figures is True:
                with open(file_to_process, 'w', encoding='UTF-8') as outfile:
                        for line in new_content:
                                outfile.write(line)
        else:
                figure_location_text = []
                for line in new_content:
                        if '![' in line:
                                line = line.replace('![','')
                                figure_name_text = line.split(']')[1].replace('(', '').replace(')', '')
                                figure_position_text = line.split(']')[0]

                                start = r'\begin{center}' + '\n'
                                middle = figure_position_text + r' \color{gray}{' + ' (figure filename: ' + figure_name_text.split('/')[1].replace('\n','').replace('_', r'\_') + ')}'
                                end = '\n' r'\end{center}' + '\n'

                                line = start + middle + end
                        figure_location_text.append(line)
                with open(file_to_process, 'w', encoding='UTF-8') as outfile:
                        for line in figure_location_text:
                                outfile.write(line)


# WORD COUNT FUNCTION

translator = str.maketrans('', '', string.punctuation)

def get_markdown_files(directory='generated_pdfs/intermediary_markdown'):
    a, _, filenames = next(walk(directory))
    files = [a + '/' + f for f in filenames if '.md' in f]
    return files

def count_words(file, end_of_metadata=37): # the metadata appended to the start of the chapter end
    with open(file, 'r', encoding='utf-8') as to_count:
        intext = to_count.readlines()
        text = []
        for line in intext[end_of_metadata:]:
            if '>**Comment (JA):**' not in line:
                if 'todo' not in line.lower():
                    if not line.startswith('<!--'):
                        text.append(line)
        text = " ".join(text)
        tokenized = text.split()
        tokenized = [word.translate(translator) for word in tokenized]
        tokenized = [word for word in tokenized if len(word)>0]
        return file.split('/')[2], len(tokenized)


# def count_words(file, end_of_metadata=37): # the metadata appended to the start of the chapter end
#     with open(file, 'r', encoding='utf-8') as to_count:
#         text = to_count.readlines()
#         text = text[end_of_metadata:]
#         text = [line for line in text if '>**Comment (JA):**' not in line]
#         text = " ".join(text)
#         tokenized = text.split()
#         tokenized = [word.translate(translator) for word in tokenized]
#         tokenized = [word for word in tokenized if len(word)>0]
#         # return tokenized
#         return file.split('/')[2], len(tokenized)



# def count_words(file):
#     with open(file, 'r', encoding='utf-8') as to_count:
#         text = to_count.read()
#         tokenized = text.split()
#         tokenized = [word.translate(translator) for word in tokenized]
#         return file.split('/')[2], len(tokenized)

def get_datetime():
    now = pd.to_datetime("today")
    now_split = str(now).split(' ')
    date = now_split[0]
    time = now_split[1].split('.')[0].replace(':','.')
    date + time
    return f'{date}[{time}]'

def get_counts(directory='generated_pdfs/intermediary_markdown'):
    files = get_markdown_files()
    word_counts = {}
    for file in files:
        fn, wc = count_words(file)
        word_counts[fn] = wc
    return word_counts

def report_progress(counts, target=210_000):
    # log progress
    report = pd.DataFrame.from_dict(counts, orient='index', columns=['Word Count'])
    # report.to_csv(f'logs/{get_datetime()}.csv')
    # print progress
    string_lens = []
    for k,v in counts.items():
        string_lens.append(len(k))
    ms = max(string_lens)+5
    total = []
    for k,v in counts.items():
        diff = ms - len(k)
        head = k + ' '*diff
        print(head, f'{v:,}')
        total.append(v)
    print(f'\n\nTotal Word Count: {sum(total)}')
    print(f'WORD DELTA: {target-sum(total)}')
    #print(report.sort_index(ascending=True))
