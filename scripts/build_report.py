"""Build the illustrated portfolio from existing figures and recorded results.

Install requirements-report.txt, then run this script from any directory.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'report'
REPORT.mkdir(exist_ok=True)
FONT_ROOT = Path(reportlab.__file__).parent/'fonts'
pdfmetrics.registerFont(TTFont('Vera',str(FONT_ROOT/'Vera.ttf')))
pdfmetrics.registerFont(TTFont('Vera-Bold',str(FONT_ROOT/'VeraBd.ttf')))
pdfmetrics.registerFont(TTFont('Vera-Italic',str(FONT_ROOT/'VeraIt.ttf')))
pdfmetrics.registerFontFamily('Vera',normal='Vera',bold='Vera-Bold',italic='Vera-Italic',boldItalic='Vera-Bold')
NAVY=colors.HexColor('#14283F')
TEAL=colors.HexColor('#137D83')
INK=colors.HexColor('#26384B')
MUTED=colors.HexColor('#566575')
PALE=colors.HexColor('#EDF5F5')
LINE=colors.HexColor('#D5E0E5')
W,H=595.276,841.89
CONTENT=W-100
styles={
 'body':ParagraphStyle('body',fontName='Vera',fontSize=9.3,leading=14.3,textColor=INK,spaceAfter=10),
 'small':ParagraphStyle('small',fontName='Vera',fontSize=8,leading=11.7,textColor=MUTED,spaceAfter=8),
 'caption':ParagraphStyle('caption',fontName='Vera',fontSize=7.7,leading=11,textColor=MUTED,spaceAfter=10),
 'h1':ParagraphStyle('h1',fontName='Vera-Bold',fontSize=22,leading=27,textColor=NAVY,spaceAfter=15),
 'h2':ParagraphStyle('h2',fontName='Vera-Bold',fontSize=11.3,leading=16,textColor=TEAL,spaceBefore=8,spaceAfter=8),
 'kicker':ParagraphStyle('kicker',fontName='Vera-Bold',fontSize=8,leading=12,textColor=TEAL,spaceAfter=9),
 'cover':ParagraphStyle('cover',fontName='Vera-Bold',fontSize=31,leading=38,textColor=NAVY,spaceAfter=18),
 'lead':ParagraphStyle('lead',fontName='Vera',fontSize=12,leading=19,textColor=INK,spaceAfter=20),
}
story=[]
markdown=['# Selected Academic Projects\n\n**Gabriel Trabelsi**\n\nM2 IASD · Université Paris Dauphine-PSL\n\n[Download the illustrated PDF](portfolio.pdf)\n']


def plain_html(s):
    return re_markdown(s)


def re_markdown(s):
    import re
    s=re.sub(r'<b>(.*?)</b>',r'**\1**',s)
    s=re.sub(r'<i>(.*?)</i>',r'*\1*',s)
    s=re.sub(r'<a href="(.*?)">(.*?)</a>',r'[\2](\1)',s)
    return s.replace('<br/>','\n\n').replace('&amp;','&').replace('&lt;','<').replace('&gt;','>')


def p(text,style='body',to_md=True):
    story.append(Paragraph(text,styles[style]))
    if to_md:
        prefix='### ' if style=='h2' else ''
        markdown.append(prefix+plain_html(text)+'\n')


def page(kicker,title):
    if story:
        story.append(PageBreak())
    p(kicker,'kicker',False)
    p(title,'h1',False)
    markdown.append('## '+title+'\n')


def fig(filename,caption,max_height=240):
    path=ROOT/'assets'/filename
    width,height=ImageReader(str(path)).getSize()
    scale=min(CONTENT/width,max_height/height)
    story.append(Image(str(path),width=width*scale,height=height*scale))
    story.append(Spacer(1,6))
    p(caption,'caption',False)
    markdown.append(f'![{caption}](../assets/{filename})\n\n*{caption}*\n')


def two_figs(left,right,caption,max_height=185):
    ims=[]
    for filename in [left,right]:
        width,height=ImageReader(str(ROOT/'assets'/filename)).getSize()
        scale=min((CONTENT-14)/2/width,max_height/height)
        ims.append(Image(str(ROOT/'assets'/filename),width=width*scale,height=height*scale))
    t=Table([ims],colWidths=[CONTENT/2]*2)
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]))
    story.append(t)
    story.append(Spacer(1,6))
    p(caption,'caption',False)
    markdown.append(f'![{caption}](../assets/{left})\n\n![{caption}](../assets/{right})\n\n*{caption}*\n')


def table(headers,rows,widths):
    data=[[Paragraph(escape(str(x)),styles['small']) for x in headers]]
    data += [[Paragraph(escape(str(x)),styles['small']) for x in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LINEBELOW',(0,0),(-1,0),.8,TEAL),('LINEBELOW',(0,1),(-1,-1),.35,LINE),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    story.append(t)
    story.append(Spacer(1,12))
    markdown.append('| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(map(str,r))+' |' for r in rows)+'\n')


# 01 / A compact overview, with a substantial figure and concrete navigation.
p('SELECTED ACADEMIC PROJECTS  /  SEPTEMBER 2026','kicker',False)
story.append(Spacer(1,17))
p('Statistical Learning<br/>&amp; Computational<br/>Statistics','cover',False)
p('Gabriel Trabelsi','h2',False)
p('M2 IASD · Université Paris Dauphine-PSL','lead',False)
p('From statistical methods to Python implementations and experimental analysis. This portfolio brings together existing coursework on sensor-based regression, Monte-Carlo simulation, Bayesian inference and latent-variable estimation.','lead')
table(['Focus','Evidence in the portfolio'],[
    ['Learning from data','Cleaning, temporal structure, regression baselines, kernels, neural networks and residual analysis.'],
    ['Computational inference','Simulation, importance weights, Metropolis/MALA and the E-step/M-step of Gaussian-mixture EM.'],
    ['Scientific interpretation','Sensitivity to hyperparameters, initialization, data size and modelling assumptions.'],
],[120,CONTENT-120])
p('Reading path','h2')
p('Air Quality: pages 2-4. Simulation and rare events: page 5. Bayesian sampling: page 6. EM: page 7. Code, provenance and reproduction: page 8.')
p('A presentation edition of completed academic work. Figures and numerical results are retained from the original notebooks; model limitations are stated alongside the observations.','small')
p('<a href="https://github.com/Frodogorn/statistical-learning-portfolio">github.com/Frodogorn/statistical-learning-portfolio</a>','small')

# 02 / Data.
page('01 / STATISTICAL LEARNING','Air-quality estimation')
p('Problem and data','h2')
p('Estimate CO, benzene, NOx and NO2 reference concentrations from five sensor responses and temperature, relative humidity and absolute humidity. This is contemporaneous sensor-based estimation, with a chronological evaluation split.')
p('The local CSV contains 9,357 dated observations. Missing values encoded as -200 are replaced, the mostly missing NMHC reference variable is removed, and complete-case filtering retains <b>6,941 observations</b>. The original split uses <b>5,552 training rows and 1,389 later evaluation rows</b>.')
fig('air_correlations.png','Figure 1. Correlations from the original exploratory analysis. Correlated sensor responses complicate coefficient interpretation.',max_height=345)
p('Implemented workflow','h2')
p('Distribution plots and temporal profiles lead into standardized linear baselines, ridge regression, RBF kernel ridge regression and dense neural networks. The analysis then inspects prediction errors, permutation importance and Kernel SHAP.')
p('Dataset: Vito, S. (2008), Air Quality, UCI Machine Learning Repository. DOI: 10.24432/C59K5F. The project retains the dataset source and its separate terms.','small')

# 03 / Actual stored values, not the stale original summary.
page('01 / STATISTICAL LEARNING','Comparing the fitted models')
p('Recorded R² on the chronological evaluation partition','h2')
table(['Target','OLS, 8 inputs','Ridge','RBF kernel','MLP (64,32)'],[
    ['CO','0.8605','0.8605','0.8769','0.8258'],
    ['Benzene','0.9429','0.9429','0.9999','0.9986'],
    ['NOx','0.8336','0.8339','0.8838','0.8961'],
    ['NO2','0.5018','0.5019','0.5606','0.6075'],
],[75,110,85,105,CONTENT-375])
p('Values are transcribed from the saved numerical outputs. The MLP column uses one fixed architecture and original settings, rather than a different winning architecture for each target. The final partition was reused for exploratory comparisons, so these are not independent final benchmark scores.','small')
fig('air_predictions.png','Figure 2. Selected predicted-versus-observed plots. The original display uses kernel models for CO/benzene and MLP models for NOx/NO2.',max_height=170)
fig('air_kernel_grid.png','Figure 3. An existing kernel hyperparameter sweep. The heatmap is a separate grid from the search reported in the table.',max_height=142)
p('Observation','h2')
p('Predictive difficulty varies markedly across targets. The benzene fit is nearly deterministic in this dataset, while NO2 remains harder to estimate. This comparison motivates inspection of errors and the experimental protocol, rather than a single headline score.')

# 04 / Interpretation.
page('01 / STATISTICAL LEARNING','Temporal structure and errors')
fig('air_monthly_profiles.png','Figure 4. Monthly concentration profiles in the cleaned data.',max_height=150)
p('Existing hour-of-day experiment','h2')
p('The notebook adds sine/cosine encodings of hour to the NO2 predictors. For the same MLP configuration, the recorded R² changes from <b>0.6698 to 0.7049</b>, a gain of 0.0351. This is an exploratory comparison following a hyperparameter sweep on the same evaluation partition.')
fig('air_residuals.png','Figure 5. NO2 residuals from the separate, deeper network with augmented inputs. These are not the residuals of every MLP in the comparison table.',max_height=185)
p('Interpretation and protocol','h2')
p('The stored residual diagnostics show a positive mean error and a heavy right tail. This supports inspecting underestimation of high concentrations. Correlation and feature attribution remain descriptive: they do not establish a causal sensor effect or automatically separate correlated inputs.')
p('The outer scaler is fitted on training data, but before inner cross-validation. RidgeCV and MLP early stopping also use their default internal validation schemes. A future independent benchmark would isolate preprocessing within folds and reserve an untouched final test set; the current edition preserves the original experiment.','small')

# 05 / Existing rare-event work.
page('02 / COMPUTATIONAL STATISTICS','Simulation and rare events')
p('From a distribution to a simulator','h2')
p('The simulation notebook implements repeated Bernoulli trials, inverse transforms, Box-Muller, Marsaglia polar sampling and a Cholesky transform for correlated Gaussian vectors. Its saved timings are illustrative individual runs; the Box-Muller and SciPy timing cells generate different numbers of output values.')
p('When direct Monte-Carlo misses the event','h2')
table(['Gaussian tail P(Z ≥ 6)','Saved value'],[
    ['Analytical reference','9.865876450376948e-10'],
    ['Direct Monte-Carlo, 100 million draws','0'],
    ['Shifted exponential, 500,000 draws','9.865407869402759e-10'],
],[CONTENT*.61,CONTENT*.39])
two_figs('gaussian_importance_sampling.png','pareto_importance_sampling.png','Figures 6-7. Running importance-sampling estimates for a Gaussian tail (left) and a Pareto tail (right).',max_height=180)
p('A proposal can also fail','h2')
p('The Pareto example uses a light-tailed exponential proposal. The saved run records a maximum-to-average weight ratio above <b>120,000</b>. Large weights can dominate the estimate, so the displayed normal-approximation interval should not be treated as validated uncertainty. These are existing individual experiments, not repeated-run coverage studies.')

# 06 / MCMC.
page('02 / COMPUTATIONAL STATISTICS','Bayesian updates and sampling')
p('A conjugate reference example','h2')
p('For a standard normal prior and Gaussian observations with unit variance, the completed integration example plots posterior densities after 3, 5 and 10 observations. It also computes the posterior mean, providing a simple reference for Bayesian estimation.')
p('Two Gaussian-target samplers','h2')
p('Random-walk Metropolis proposes a symmetric uniform increment and applies the target-density ratio. MALA uses the Gaussian log-density gradient to move toward the central region, then corrects for the asymmetric proposal. The functions return samples and acceptance rates.')
two_figs('gaussian_posterior.png','metropolis_histogram.png','Figures 8-9. Conjugate Gaussian posterior updates (left) and a Metropolis Gaussian-target histogram (right), from the original notebooks.',max_height=210)
p('What is demonstrated','h2')
p('The completed code makes proposal construction, acceptance logic and the effect of initialization explicit. An additional section retains the original posterior-sampling implementation for a mixture weight, with its inconsistent historical outputs omitted.')
p('What is not established','h2')
p('Marginal histograms and acceptance rates are limited diagnostics. The original work does not report effective sample size, multi-chain convergence checks or a computation-normalized comparison. Direct evaluation of small densities can also cause underflow.')

# 07 / EM.
page('02 / COMPUTATIONAL STATISTICS','Latent-variable estimation with EM')
p('Implemented model','h2')
p('A two-component univariate Gaussian mixture is fitted by alternating responsibilities and weighted parameter updates. The code estimates the mixture weight, both means and separate component variances. The original simulation uses means -2 and 3, standard deviations 1.5 and 1, and weight 0.3.')
fig('em_convergence.png','Figure 10. Original parameter trajectories and observed log-likelihood.',max_height=235)
fig('em_initialization.png','Figure 11. Existing initialization experiment on the same sample.',max_height=125)
p('Existing sensitivity experiments','h2')
p('A reusable EM function supports changes in initialization, iteration count and sample size. Another experiment deliberately fits two components to data generated from three groups. These examples expose sensitivity and model misspecification; a likelihood plateau alone does not establish a globally optimal or appropriate fit.')
p('Implementation limits: fixed iteration budgets, direct density calculations and no variance floor. Sample-size comparisons use one new sample per size.','small')

# 08 / Handoff for recruiter/technical reader.
page('03 / CODE AND CONTEXT','Inspecting and reproducing the work')
p('Notebook guide','h2')
table(['Notebook','Content'],[
    ['01_air_quality','Exploratory analysis, regressors, interpretation and residuals.'],
    ['02_random_variable_simulation','Geometric and Gaussian simulation.'],
    ['03_rare_event_estimation','Gaussian/Pareto tails and importance weights.'],
    ['04_gaussian_bayes','Completed conjugate Gaussian example.'],
    ['05_metropolis_and_mala','Gaussian samplers and supplementary posterior code.'],
    ['06_expectation_maximization','Mixture EM and its existing sensitivity experiments.'],
    ['07_hamiltonian_monte_carlo','Leapfrog integrator, HMC and MALA compared with Metropolis.'],
    ['08_variational_inference','CAVI for a Gaussian mixture, compared with Metropolis.'],
],[195,CONTENT-195])
p('Academic provenance','h2')
p('The portfolio presents Gabriel Trabelsi’s completed coursework implementations and experiments within supplied teaching frameworks. The earlier UM4MA379 TP1-TP3 notebooks are from Sorbonne Université, Master 1, 2025-2026, with A. Guyader credited for the course and M. Sangnier for the practical sessions. The current M2 IASD affiliation does not change that provenance.')
p('TP6, TP7 and TP8 are credited to the supplied Statistiques computationnelles practical notebooks; individual instructor names are not inferred. Course handouts, provided corrections, empty templates and duplicate submissions are not republished. The completed TP6 leapfrog integrator, HMC loop and two-dimensional MALA are presented in the HMC notebook; helper functions are also retained separately. The completed TP8 variational-inference practical has its own notebook.')
p('Reproduction and presentation','h2')
p('The repository supplies data, dependencies, source-cell mapping, methodology notes and executable checks. Large sampling cells and the full Air Quality searches retain their original settings. Saved outputs and figure files are historical results, except the HMC and variational-inference notebook outputs, regenerated by re-execution; validation runs do not overwrite them. See docs/validation.md for the exact validation scope.')
p('The presentation changes include clearer organization, English explanations, relative data loading and corrected narrative transcription. An unused scalar sampling helper receives its missing size argument. No new algorithms or experimental extensions are claimed.','small')
p('<a href="https://github.com/Frodogorn/statistical-learning-portfolio">github.com/Frodogorn/statistical-learning-portfolio</a>','small')


def footer(canvas,doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFont('Vera',7)
        canvas.setFillColor(MUTED)
        canvas.drawString(50,H-33,'GABRIEL TRABELSI  /  SELECTED ACADEMIC PROJECTS')
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(.5)
    canvas.line(50,43,W-50,43)
    canvas.setFont('Vera',7)
    canvas.setFillColor(MUTED)
    canvas.drawString(50,29,'Statistical Learning & Computational Statistics')
    canvas.drawRightString(W-50,29,f'{doc.page:02d}')
    canvas.restoreState()


if __name__=='__main__':
    doc=SimpleDocTemplate(str(REPORT/'portfolio.pdf'),pagesize=(W,H),leftMargin=50,rightMargin=50,topMargin=58,bottomMargin=59,
        title='Selected Academic Projects - Statistical Learning and Computational Statistics',author='Gabriel Trabelsi',
        subject='Academic portfolio: statistical learning, simulation and probabilistic inference')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    (REPORT/'portfolio.md').write_text('\n'.join(markdown)+'\n',encoding='utf-8')
    print(REPORT/'portfolio.pdf')
