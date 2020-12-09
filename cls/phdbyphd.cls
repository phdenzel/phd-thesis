% phdbyphd.cls
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cls/phdbyphd}[2020/06/09 valpha-1.0 phdbyphd]

\newcommand{\@classname}{phdbyphd}
\newcommand{\@baseclass}{scrbook}

% Defaults
\PassOptionsToClass{fontsize=9.5pt}{\@baseclass}
\PassOptionsToClass{parskip=half}{\@baseclass}
\PassOptionsToClass{headings=optiontoheadandtoc}{\@baseclass}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{\@baseclass}}

\ProcessOptions\relax

\LoadClass{\@baseclass}
\RequirePackage{styles/phdbyphd} % Load class style


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Front/Main/Back/Appendix

\newlength{\overflowingheadlen}

\let\basefrontmatter\frontmatter  % customize frontmatter cmd
\renewcommand{\frontmatter}{
	\basefrontmatter

	\setlength{\overflowingheadlen}{\linewidth}
	\addtolength{\overflowingheadlen}{\marginparsep}
	\addtolength{\overflowingheadlen}{\marginparwidth}

	\pagestyle{plain.scrheadings}
	\pagelayout{wide}
	% \sloppy
}

\let\basemainmatter\mainmatter % customize mainmatter cmd
\renewcommand{\mainmatter}{

	% comment out what you need if page numbering doesn't work
	\afterpage{\blankpage}
	%\afterpage{\blankpage}
	%\afterpage{\blankpage}
	\Ifthispageodd{%\ifthispageodd{
		\afterpage{\blankpage}%\addtocounter{page}{-1}
	}{
		% \afterpage{\blankpage}%\addtocounter{page}{-1}
	}
	
	\basemainmatter

	\setlength{\overflowingheadlen}{\linewidth}
	\addtolength{\overflowingheadlen}{\marginparsep}
	\addtolength{\overflowingheadlen}{\marginparwidth}

	\pagestyle{scrheadings}
	\pagelayout{margin}
}

\let\baseappendix\appendix % customize appendix cmd
\renewcommand{\appendix}{
	\baseappendix
	\bookmarksetup{startatroot}
}

\let\basebackmatter\backmatter % customize backmatter cmd
\renewcommand{\backmatter}{
	\basebackmatter

	\setlength{\overflowingheadlen}{\linewidth}
	\addtolength{\overflowingheadlen}{\marginparsep}
	\addtolength{\overflowingheadlen}{\marginparwidth}

	\bookmarksetup{startatroot}
	\pagestyle{plain.scrheadings}
	\pagelayout{wide}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Chapter headings

% Style option selector
\DeclareDocumentCommand{\setchapterstyle}{m}{%
	\ifthenelse{\equal{plain}{#1}}{\chapterstyleplain}{}
	\ifthenelse{\equal{lines}{#1}}{\chapterstylelines}{}
	\ifthenelse{\equal{phdbyphd}{#1}}{\chapterstylephdbyphd}{}
}
% plain option
\DeclareDocumentCommand{\chapterstyleplain}{}{%
	\renewcommand{\chapterlinesformat}[3]{%
		\@hangfrom{##2}{##3}}
	\renewcommand*{\chapterformat}{%
		\mbox{\chapappifchapterprefix{\nobreakspace}\thechapter%
		\autodot\IfUsePrefixLine{}{\enskip}}}
	\RedeclareSectionCommand[beforeskip=0cm,afterskip=1cm]{chapter}
	\setlength{\mtocshift}{-3.2cm}
}
% phdbyphd option
\DeclareDocumentCommand{\chapterstylephdbyphd}{}{%
	\renewcommand*{\chapterformat}{%
		\mbox{\chapappifchapterprefix{\nobreakspace}\scalebox{2.85}{\thechapter\autodot}}%
	}
	\renewcommand\chapterlinesformat[3]{%
		\vspace*{-4.5cm}%
		\makebox[\textwidth+\marginparsep+\marginparwidth]{%
			\parbox[b]{\textwidth}{\flushright{##3}}%
			\makebox[\marginparsep][c]{\rule[-.2cm]{1pt}{5.7cm}}%
			\parbox[b]{\marginparwidth}{##2}%
		}
	}
	\RedeclareSectionCommand[beforeskip=0cm,afterskip=1cm]{chapter}
	\setlength{\mtocshift}{0mm}
}
% lines option
\renewcommand{\hrulefill}[1][0.4pt]{%
	\leavevmode\leaders\hrule height #1\hfill\kern\z@%
}
\DeclareDocumentCommand{\chapterstylelines}{}
{
	\renewcommand*{\chapterformat}
	{
	  \chapappifchapterprefix{\nobreakspace}\scalebox{3.5}{\thechapter\autodot}
	}
	\renewcommand\chapterlinesformat[3]
	{
	  \leavevmode
	  \makebox[\textwidth+\marginparsep+\marginparwidth]{%
		\makebox[\textwidth][l]{\hrulefill[1pt]##2}%
		\makebox[\marginparsep][l]{}%
		\makebox[\marginparwidth][l]{}%
	  }\\
	  %\vspace{.5cm}
	  \makebox[\textwidth+\marginparsep+\marginparwidth]{%
		\makebox[\textwidth][l]{##3}%
		\makebox[\marginparsep][l]{}%
		\makebox[\marginparwidth][l]{}%
	  }\\
	  \makebox[\textwidth+\marginparsep+\marginparwidth]{%
		\hrulefill[1.1pt]%
	  }
	}
	\RedeclareSectionCommand[beforeskip=0cm,afterskip=1cm]{chapter}
	\setlength{\mtocshift}{-2.5cm}
}

% Cool images at the beginning of the chapter
\DeclareDocumentCommand{\chapterstyleimage}{}{%
	\renewcommand*{\chapterformat}{%
		\mbox{\chapappifchapterprefix{\nobreakspace}\thechapter%
		\autodot\IfUsePrefixLine{}{\enskip}}
	}
	\renewcommand{\chapterlinesformat}[3]{%
		\begin{tikzpicture}[remember picture, overlay]
			\node[
				anchor=west,
				xshift=-3cm,
				yshift=1.15cm,
				rectangle,
				fill=gray!20!white,
				fill opacity=0.8,
				inner ysep=14pt,
				inner xsep=3cm,
				text opacity=1,
				text width=\paperwidth+3cm,
			]{\makebox[0pt][l]{\@hangfrom{##2}{##3}}};
			\node[
				anchor=west,
				xshift=-3cm,
				yshift=2mm,
				rectangle,
				fill=white,
				minimum height=.5cm,
				minimum width=\paperwidth+3cm,
			]{};
		\end{tikzpicture}
	}
}
% Command declaration
\DeclareDocumentCommand{\setchapterimage}{O{5.5cm} m}{%
	\setchapterpreamble[o]{%
		\vspace*{-2.7cm}\hspace*{-2.5cm}%
		\includegraphics[width=\paperwidth,height=#1+2.7cm,keepaspectratio=false]{#2}%
	}%
	\chapterstyleimage%
	% beforeskip=-(figure_height-top_margin)
	\RedeclareSectionCommand[beforeskip=-#1, afterskip=.6cm]{chapter}%
	\setlength{\mtocshift}{0cm}%
}

% By default start with plain style
\chapterstyleplain

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% KOMA fonts

% for all elements
\addtokomafont{section}{\normalfont\bfseries}
\addtokomafont{subsection}{\normalfont\bfseries}
\addtokomafont{subsubsection}{\normalfont\bfseries}
\addtokomafont{paragraph}{\normalfont\bfseries}
\setkomafont{descriptionlabel}{\normalfont\bfseries}

% for book-specific elements
\addtokomafont{part}{\normalfont\scshape\bfseries}
\addtokomafont{partentry}{\normalfont\scshape\bfseries}
\addtokomafont{chapter}{\normalfont\bfseries}
\addtokomafont{chapterentry}{\normalfont\bfseries}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TOC

\PassOptionsToClass{toc=listof}{\@baseclass}
\PassOptionsToClass{toc=index}{\@baseclass}
\PassOptionsToClass{toc=bibliography}{\@baseclass}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Counters

\setcounter{secnumdepth}{2}
\counterwithin*{sidenote}{chapter} % for global counter: \counterwithout{sidenote}{chapter}
