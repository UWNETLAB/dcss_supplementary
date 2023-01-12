import os
import pandas as pd
import numpy as np
import string
import html2text
import yaml

def get_chapter_files(directory='.', ext='.ipynb'):
    chapters = []
    a, _, filenames = next(os.walk(directory))
    for f in filenames:
        if 'chapter_' in f:
            if ext in f:
                chapters.append(f'{a}/{f}')
    mds = [file.replace('.ipynb','.md') for file in chapters]
    return chapters, mds

def load_metadata(metadata='meta.md'):
    with open('templates/meta.md', 'r') as f:
        meta = f.readlines()
        title_string_corrected = []
        for line in meta:
            if line.startswith('title: '):
                line = line.replace('title: ', 'title: "')
                line = line.replace('\n', '') + '"' + '\n'
            title_string_corrected.append(line)
        meta = "".join(title_string_corrected)
    return meta

def load_chapter(chapter):
    meta = load_metadata()
    html = os.popen(f'pandoc {chapter} -o /dev/stdout').read()
    text = html2text.html2text(html).split('\n')
    text = [t for t in text if len(t) > 0]
    text.insert(0, load_metadata())
    return text

def process_markdown(chapter, replacements=[]):
    with open(chapter, 'r') as f:
        c_number = chapter.split('_')[1]

        lines = f.readlines()
        body = []

        # replacements and filters
        for line in lines[1:]:
            if '/home/' not in line:
                if 'and should_run_async(code)' not in line:
                    if 'pd.set_option("display.notebook_repr_html", False)' not in line:
                        for r in replacements:
                            if r[0] in line:
                                line = line.replace(r[0], r[1])

#                         if '../figures/' in line:
#                             line = line.replace('../figures/', 'figures/')

                        body.append(line)

        title = lines[0].replace('# <font color="#49699E" size=40>', '').replace('</font>', '').strip()
        #title = title.split(':', 1) # split on first occurrence only
        #c_number = title[0]
        c_string = title
        #c_string = title[1].strip()

        # METADATA SHIT
        meta = load_metadata()
        meta = meta.replace('CHAPTER_TITLE', title.strip())

        contents = [meta] + body

    with open(chapter, 'w') as f:
        f.write("".join(contents))

## BEFORE THAT NEW PANDAS FILTER FOR
# pd.set_option("display.notebook_repr_html

# def process_markdown(chapter, replacements=[]):
#     with open(chapter, 'r') as f:
#         c_number = chapter.split('_')[1]

#         lines = f.readlines()
#         body = []

#         # replacements and filters
#         for line in lines[1:]:
#             if '/home/' not in line:
#                 if 'and should_run_async(code)' not in line:
#                     for r in replacements:
#                         if r[0] in line:
#                             line = line.replace(r[0], r[1])

#                     if '../figures/' in line:
#                         line = line.replace('../figures/', 'figures/')

#                     body.append(line)

#         title = lines[0].replace('# <font color="#49699E" size=40>', '').replace('</font>', '').strip()
#         #title = title.split(':', 1) # split on first occurrence only
#         #c_number = title[0]
#         c_string = title
#         #c_string = title[1].strip()

#         # METADATA SHIT
#         meta = load_metadata()
#         meta = meta.replace('CHAPTER_TITLE', title.strip())

#         contents = [meta] + body

#     with open(chapter, 'w') as f:
#         f.write("".join(contents))




def prepare_for_book_build(chapter, replacements = []):
    # in case you pass a notebook instead, DO NOT overwrite the notebook with some bullshit
    if 'ipnb' in chapter:
        chapter = chapter.replace('ipynb', 'md')

    adjusted = []
    with open(chapter, 'r') as f:
        lines = f.readlines()
        adjusted.append(lines[0].replace('<font color="#49699E" size=40>', '').replace('</font>', ''))
        for line in lines[1:]: # exclude the title
            # REPLACEMENTS
            if '/home/' not in line:
                if 'and should_run_async(code)' not in line:
                    for r in replacements:
                        if r[0] in line:
                            line = line.replace(r[0], r[1])

                    # ADJUST HEADERS AND UPDATE FIGURES PATH
                    if line.startswith('##### '):
                        line = line.replace('##### ', '###### ')
                    if line.startswith('#### '):
                        line = line.replace('#### ', '##### ')
                    if line.startswith('### '):
                        line = line.replace('### ', '#### ')
                    if line.startswith('## '):
                        line = line.replace('## ', '### ')
                    if line.startswith('# '):
                        line = line.replace('# ', '## ').upper()

#                     if '../figures/' in line:
#                         line = line.replace('figures/', '../images/')
                    #if 'figures/' in line:
                    #    line = line.replace('figures/', '../images/')

                    if '.svg' in line:
                        print(f'\n\n\n\n\nTHERE IS A GODDAMN SVG IN HERE!\n{line}\n\n\n\n\n')
                        line = ""
                    adjusted.append(line)

    adjusted.append('')
    adjusted.append(r'\newpage')
    adjusted.append('')

    with open(chapter, 'w') as f:
        f.write("".join(adjusted))








def concatenate_meta_chapter(title, body, replacements=[[r'\text{test_prior}', r'\text{test\_prior}'],
                                                       [r'text{another_test}', r'text{another\_test}']], write=True):
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

# def append_metadata(chapter):
#     meta = load_metadata()
#     with open(chapter, 'rw') as f:
#         lines = f.readlines()
#         body = []
#         for line in lines[1:]:
#             for r in replacements:
#                 if r[0] in line:
#                     line = line.replace(r[0], r[1])
#             if '../figures/' in line:
#                 line = line.replace('../figures/', '../../figures/')
#             body.append(line)
#         #body = lines[1:]

#         title = lines[0].replace('# <font color="#49699E" size=40>',
#                                  '').replace('</font>', '')
#         title = title.split(':', 1) # split on first occurrence only
#         c_number = title[0]
#         c_string = title[1].strip()





# def parse_chapter(markdown):
#     with open(markdown, 'r') as f:
#         lines = f.readlines()
#         body = []
#         for line in lines[1:]:
#             for r in replacements:
#                 if r[0] in line:
#                     line = line.replace(r[0], r[1])
#             if '../figures/' in line:
#                 line = line.replace('../figures/', '../../figures/')
#             body.append(line)
#         #body = lines[1:]

#         title = lines[0].replace('# <font color="#49699E" size=40>',
#                                  '').replace('</font>', '')
#         title = title.split(':', 1) # split on first occurrence only
#         c_number = title[0]
#         c_string = title[1].strip()





def count_words(text, end_of_metadata=13):
    translator = str.maketrans('', '', string.punctuation)
    chap = {}
    intext = text
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
    return len(tokenized)


def process_chapters(list_of_chapter_files):
    counts = {}
    for chapter in list_of_chapter_files:
        fulltitle = chapter.split('/')[1].split('.')[0]
        number = fulltitle.split('_')[1]
        text = load_chapter(chapter)
        count = count_words(text)
        print(number)
        counts[int(number)] = count
    c = pd.DataFrame.from_dict(counts, orient='index')
    c.sort_index(inplace=True)
    c.columns = ['Accurate Word Count']

    t = get_targets()
    df = pd.concat([c,t], axis=1)
    df['Diff'] = df['Accurate Word Count'] - df['Target']
    return df, df['Target'].sum(), df['Accurate Word Count'].sum()

def get_targets(file='targets.yaml'):
    target_lens = {}
    with open(file, 'r') as f:
        targets = yaml.load(f, Loader=yaml.FullLoader)
        for i,t in enumerate(targets.split(' ')):
            split = t.split(':')
            target = int(split[1])
            target_lens[i+1] = target
    df = pd.DataFrame.from_dict(target_lens, orient='index')
    df.columns = ['Target']
    return df







# import pandas as pd
# import os
# from os import walk
# import shutil
# import string
# import seaborn as sns
# import matplotlib.pyplot as plt
# from dcss.plotting import custom_seaborn
# custom_seaborn()

# replacements = [
#     #[r'_', r'\_'],
#     [r'α', r'$\alpha$'],
#     [r'β', r'$\beta$'],
#     [r'γ', r'$\gamma$'],
#     [r'δ', r'$\delta$'],
#     [r'ϵ', r'$\epsilon$'],
#     [r'ε', r'$\epsilon$'],
#     [r'ζ', r'$\zeta$'],
#     [r'η', r'$\eta$'],
#     [r'θ', r'$\theta$'],
#     [r'ϑ', r'$\theta$'],
#     [r'λ', r'$\lambda$'],
#     [r'μ', r'$\mu$'],
#     [r'τ', r'$\tau$'],
#     [r'ϕ', r'$\phi$'],
#     [r'φ', r'$\phi$'],
#     [r'χ', r'$\chi$'],
#     [r'ψ', r'$\psi$'],
#     [r'ω', r'$\omega'],
#     [r'\text{test_prior}', r'\text{test\_prior}'],
#     [r'text{another_test}', r'text{another\_test}']
# ]

# def get_chapter_files(directory='.', ext='.ipynb'):
#     chapters = []
#     a, _, filenames = next(walk(directory))
#     for f in filenames:
#         if 'chapter_' in f:
#             if ext in f:
#                 chapters.append(f'{a}/{f}')
#     return chapters


# def convert_chapters_to_markdown(move=False):
#     """
#     1. Converts all chapter notebooks to markdown
#     2. Moves the markdown files and the associated chapter files to generated

#     Note that if there are old versions of those files in generated, it deletes them.
#     Returns the core string of the chapter titles for futher processing.
#     """
#     os.system(r'jupyter nbconvert --to markdown chapter_*.ipynb')

#     chapters = get_chapter_files()
#     chapter_strings = []

#     for c in chapters:
#         chapter_string = c.split('.ipynb')[0].split('/')[1]
#         chapter_strings.append(chapter_string)

#         if os.path.exists(f'{chapter_string}.md'):
#             if os.path.exists(f'generated/{chapter_string}.md'):
#                 os.remove(f'generated/{chapter_string}.md')
#             shutil.move(f'{chapter_string}.md',
#                         f'generated/{chapter_string}.md')
#         else:
#             print(f'Potential problem with: {chapter_string}')

#         if os.path.exists(f'{chapter_string}_files'):
#             if os.path.exists(f'generated/{chapter_string}_files'):
#                 os.system(f'rm -rf generated/{chapter_string}_files')
#             try:
#                 shutil.move(f'{chapter_string}_files', f'generated/{chapter_string}_files')
#             except Exception as e: print(e)

#     chapter_paths = [f'generated/{c}.md' for c in chapter_strings]
#     return chapter_paths

# def load_metadata(metadata='meta.md'):
#     with open('templates/meta.md', 'r') as f:
#         meta = f.readlines()
#         title_string_corrected = []
#         for line in meta:
#             if line.startswith('title: '):
#                 line = line.replace('title: ', 'title: "')
#                 line = line.replace('\n', '') + '"' + '\n'
#             title_string_corrected.append(line)
#         meta = "".join(title_string_corrected)
#     return meta


# def parse_chapter(markdown):
#     with open(markdown, 'r') as f:
#         lines = f.readlines()
#         body = []
#         for line in lines[1:]:
#             for r in replacements:
#                 if r[0] in line:
#                     line = line.replace(r[0], r[1])
#             if '../figures/' in line:
#                 line = line.replace('../figures/', '../../figures/')
#             body.append(line)
#         #body = lines[1:]

#         title = lines[0].replace('# <font color="#49699E" size=40>',
#                                  '').replace('</font>', '')
#         title = title.split(':', 1) # split on first occurrence only
#         c_number = title[0]
#         c_string = title[1].strip()
#     return c_number, c_string, body, markdown


# def append_chapter_metadata(title,body):
#     meta = load_metadata()
#     meta = meta.replace('CHAPTER_TITLE', title.replace('\n', ''))
#     chapter = meta + '\n\n' + "".join(body)
#     #chapter = '---\n' + meta + '\n---\n\n' + "".join(body)
#     return chapter


# def process_chapter(chapter):
#     number, title, body, file = parse_chapter(chapter)
#     processed = append_chapter_metadata(title, body)

#     if os.path.exists(file):
#         os.remove(file)
#         with open(file, 'w') as f:
#             f.write(processed)


# def count_words(file, end_of_metadata=13): # the metadata appended to the start of the chapter end
#     translator = str.maketrans('', '', string.punctuation)
#     with open(file, 'r', encoding='utf-8') as to_count:
#         chap = {}
#         intext = to_count.readlines()
#         text = []
#         for line in intext[end_of_metadata:]:
#             if '>**Comment (JA):**' not in line:
#                 if 'todo' not in line.lower():
#                     if not line.startswith('<!--'):
#                         text.append(line)
#         text = " ".join(text)
#         tokenized = text.split()
#         tokenized = [word.translate(translator) for word in tokenized]
#         tokenized = [word for word in tokenized if len(word)>0]
#         f = file.split('/')#[1].split('_')
#         f = " ".join(f[:2]).title()
#         chap['Chapter'] = f
#         chap['Word Count'] = len(tokenized)
#         return chap
