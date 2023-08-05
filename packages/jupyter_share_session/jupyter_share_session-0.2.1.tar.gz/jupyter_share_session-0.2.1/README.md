
# Use cases

1. You want to split up your notebook into multiple files. Simply create a file "index.ipynb" in the directory where the files will be.
    - When you open a file in this directory, it will share the same session (same running kernel) as all the others
    - If the url path of the file you open is originally
        
            http://<hostname>:<port>/notebooks/<projectpath>/<file>.ipynb
      then it will be changed to 

            http://<hostname>:<port>/notebooks/<projectpath>/index.ipynb=<projectpath>/<file>.ipynb

2. You have some common files that you want to share among multiple projects (i.e. in multiple notebook directories).  You can open the common file using url path:

            <projectpath>/index.ipynb=<commonutilpath>/<utilfile>.ipynb
    - The utilfile.ipynb page will run in the same kernel.
    - The simple way to make this url path is to use a relative path from within a Markdown cell in the index.ipynb. Use this Markdown link:
    
            [utilfile](../commonutildir/utilfile)

3. You have a website full of documentation notebooks, and you want your readers to browse the documentation without first downloading all the documentation files.
    - First, create index.pynb file, with `http://` links to the documentation notebooks on your website.  The format of the links will be:
    
            <basedocpath>/index.ipynb=http://<yourwebsite>/<docpath>/<docfile>.ipynb
    - Then your users can choose to download the index.ipynb, and open it in their local jupyter.
    - Alternatively, you can put your index.ipynb file on a hosted jupyter environment (such as [Binder](http://mybinder.org/)), and have your users open the link to index.ipynb running on that environment.


# New behavior

In any of the 3 use cases:
- the window url for these notebooks will be 

            http://<host>:<port>/notebooks/<projectpath>/index.ipynb=<notebookurl>
- all lrunning notebooks with the same `<projectpath>/index.ipynb=` will run within the same kernel
- the window title for these notebooks will be "projectdir:notebookname"


# Installation


```python
!pip install jupyter_share_session
```

Add the following line to `~/.jupyter/jupyter_notebook_config.json`:

        {
          "NotebookApp": {
        ...
            "nbserver_extensions": {
        ...
              "jupyter_share_session": true
            }
          }
        }


# Example notebooks

TBD

# Issues

1. Downloading urls may not be working completely.
- The implementation is necessarily fragile and dependent on implementation details of Jupyter notebook.
    - It would be better if this behavior was included in JupyterLab directly, or there would be cleaner hooks to implement this as an extension.
- Integration with mybinder.org
- Conda installation?
- Integration with jupyter_contrib_extensions?

# Generate README


```python
!pwd
```

    /home/wayne/jupyter_share_session



```python
!jupyter nbconvert --to md index.ipynb
```

    /bin/sh: 1: nbconvert: not found


# Commit


```python
!git stage setup.py
!git commit -m 'update v0.2'
!git push -u origin master
```

    [master e0b3b5c] update v0.2
     1 file changed, 1 insertion(+), 1 deletion(-)
    Counting objects: 3, done.
    Delta compression using up to 2 threads.
    Compressing objects: 100% (3/3), done.
    Writing objects: 100% (3/3), 282 bytes | 0 bytes/s, done.
    Total 3 (delta 2), reused 0 (delta 0)
    remote: Resolving deltas: 100% (2/2), completed with 2 local objects.[K
    To https://github.com/waynebliu/jupyter_share_session.git
       1259434..e0b3b5c  master -> master
    Branch master set up to track remote branch master from origin.


# Release


```python
`372/36
```




    10.333333333333334




```python
!python setup.py sdist upload
```

    running sdist
    running egg_info
    writing jupyter_share_session.egg-info/PKG-INFO
    writing dependency_links to jupyter_share_session.egg-info/dependency_links.txt
    writing top-level names to jupyter_share_session.egg-info/top_level.txt
    reading manifest file 'jupyter_share_session.egg-info/SOURCES.txt'
    reading manifest template 'MANIFEST.in'
    writing manifest file 'jupyter_share_session.egg-info/SOURCES.txt'
    warning: sdist: standard file not found: should have one of README, README.rst, README.txt
    
    running check
    creating jupyter_share_session-0.2
    creating jupyter_share_session-0.2/jupyter_share_session
    creating jupyter_share_session-0.2/jupyter_share_session.egg-info
    copying files to jupyter_share_session-0.2...
    copying MANIFEST.in -> jupyter_share_session-0.2
    copying README.md -> jupyter_share_session-0.2
    copying setup.py -> jupyter_share_session-0.2
    copying jupyter_share_session/__init__.py -> jupyter_share_session-0.2/jupyter_share_session
    copying jupyter_share_session/sharesession.html -> jupyter_share_session-0.2/jupyter_share_session
    copying jupyter_share_session.egg-info/PKG-INFO -> jupyter_share_session-0.2/jupyter_share_session.egg-info
    copying jupyter_share_session.egg-info/SOURCES.txt -> jupyter_share_session-0.2/jupyter_share_session.egg-info
    copying jupyter_share_session.egg-info/dependency_links.txt -> jupyter_share_session-0.2/jupyter_share_session.egg-info
    copying jupyter_share_session.egg-info/not-zip-safe -> jupyter_share_session-0.2/jupyter_share_session.egg-info
    copying jupyter_share_session.egg-info/top_level.txt -> jupyter_share_session-0.2/jupyter_share_session.egg-info
    Writing jupyter_share_session-0.2/setup.cfg
    Creating tar archive
    removing 'jupyter_share_session-0.2' (and everything under it)
    running upload
    Submitting dist/jupyter_share_session-0.2.tar.gz to https://upload.pypi.org/legacy/
    Server response (200): OK

