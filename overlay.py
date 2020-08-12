from nilearn import plotting 
from glob import glob 
import os
import argparse
from jinja2 import Template

def generate_overlay_figure(overlay,background,subject, output_dir):
    if 'sub' not in subject:
        subject = 'sub-'+subject

    html_view = plotting.view_img(overlay,background,opacity=0.5,title=subject)
    html_view.save_as_html(os.path.join(output_dir,'work/'+subject+'_viewer.html'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='generating html figures')
    parser.add_argument('overlay_pattern_path',nargs=1,help="Overlay pattern path, for ambigous portions of path use '%' symbol  ie. '~/scratch/Bids_dir/sub-%/anat/sub%mask.nii.gz'")
    parser.add_argument('background_pattern_path',nargs=1,help="Background image pattern path, for abiguous portions of path use '%' ie.  '~/scratch/mask_dir/sub-%/anat/sub%_T1w.nii.gz")
    parser.add_argument('output_dir',type=str,nargs=1,help="Output directory path")
    parser.add_argument('--subs', nargs='*',help="Add in subjects to be visualized")
    args = parser.parse_args()

    overlay_paths = glob(args.overlay_pattern_path[0].replace('%','*'))
    background_paths = glob(args.background_pattern_path[0].replace('%','*'))
    output_dir = args.output_dir[0]
    
    if os.path.exists(os.path.join(output_dir,'work')) == False:
        os.makedirs(os.path.join(output_dir,'work'))
    if args.subs == None:
        subjects = [[x for x in path.split('/') if 'sub' in x][0] for path in overlay_paths]
    else:
        subjects = args.subs

        
    for sub in subjects:
        if os.path.exists(os.path.join(output_dir,'/work/'+sub+'_viewer.html')) == False:
            generate_overlay_figure([path for path in overlay_paths if sub in path][0],[path for path in background_paths if sub in path][0],sub,output_dir)
        else:
            continue

    template = Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Skull Stripped Image Reports</title>
    </head>
    <body>
    {% for sub in subjects %}
        <iframe src="./work/{{sub}}_viewer.html" width=500 height=200
        style="padding:0; border:0; display: block;
        margin-left: auto; margin-right: auto"></iframe>
    {%- endfor %}
    </body>
    </html>
    """)
    report_html_code = template.render(subjects=subjects,out_path=output_dir)
    
    with open(os.path.join(output_dir,'skstrip_report.html'),"w") as html_file:
        htmlfile.write(report_html_code)
    # path_dict = dict(zip(overlay_paths,background_paths))

    # print(path_dict)
    
    # overlay = sys.argv[1]
    # background = sys.argv[2]
    # output_dir = sys.argv[3]

    # print(sys.argv[1])                 

    # for path in overlay:
        # sub = [x for x in path.split('/') if 'sub' in x][0]

    # overlay_pattern = sys.argv[3]

    # participants_df = pd.to_csv(os.path.join(overlay_bids_dir,'participants.tsv'),sep='\t')
    # subjects = participants_df.participant_id.tolist()

    

    

