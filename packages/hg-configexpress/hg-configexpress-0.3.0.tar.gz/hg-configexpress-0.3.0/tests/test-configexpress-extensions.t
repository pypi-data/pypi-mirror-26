#require killdaemons

prepare serverhook to show config that was sent
  $ cat >> serverhook.py << EOF
  > def ourserverhook(ui, repo, **kwargs):
  >     htype = kwargs.get('hooktype')
  >     for (k, v) in sorted(kwargs.items()):
  >         if k.startswith('CLIENT'):
  >             print('%s-hookarg: %s - %s' % (htype, k, v))
  >     return 0
  > EOF
  $ cat >> testextension1.py << EOF
  > __version__ = "4.2.1337"
  > EOF
  $ cat >> testextension2.py << EOF
  > # no declared version
  > EOF

  $ export PYTHONPATH=$TESTTMP:$PYTHONPATH

  $ cat >> $HGRCPATH << EOF
  > [ui]
  > ssh=python "$RUNTESTDIR/dummyssh"
  > [extensions]
  > configexpress = $(dirname $TESTDIR)/hgext3rd/configexpress.py
  > rebase=
  > hgext.share=
  > ext1=$TESTTMP/testextension1.py
  > ext2=$TESTTMP/testextension2.py
  > [configexpress]
  > share-extensions = yes
  > EOF

setup server

  $ hg init serverrepo --traceback
  $ cat >> serverhgrc << EOF
  > [hooks]
  > pretxnchangegroup.serverhook = python:$TESTTMP/serverhook.py:ourserverhook
  > pretxnclose.serverhook = python:$TESTTMP/serverhook.py:ourserverhook
  > EOF
  $ cp serverhgrc serverrepo/.hg/hgrc
  $ hg init clientrepo
  $ cd clientrepo
  $ echo a > a
  $ hg add a
  $ hg commit -m A0
  $ echo b > b
  $ hg add b
  $ hg commit -m B0
  $ cd ..

setup clients

  $ hg clone --pull serverrepo client-up-to-date
  no changes found
  updating to branch default
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg clone --pull serverrepo --config format.usedotencode=no --config format.generaldelta=no client-multiple-deficiencies
  no changes found
  updating to branch default
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved

check value on push

  $ cd client-up-to-date
  $ echo c > c
  $ hg add c
  $ hg commit -m C0

#if hg42

  $ hg push
  pushing to $TESTTMP/serverrepo
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  pretxnchangegroup-hookarg: CLIENTCONFIG_hgversion - * (glob)
  pretxnchangegroup-hookarg: CLIENTEXTENSION_configexpress - * (glob)
  pretxnchangegroup-hookarg: CLIENTEXTENSION_ext1 - 4.2.1337
  pretxnchangegroup-hookarg: CLIENTEXTENSION_ext2 - unknown
  pretxnchangegroup-hookarg: CLIENTEXTENSION_rebase - hg-* (glob)
  pretxnchangegroup-hookarg: CLIENTEXTENSION_share - hg-* (glob)
  pretxnclose-hookarg: CLIENTCONFIG_hgversion - * (glob)
  pretxnclose-hookarg: CLIENTEXTENSION_configexpress - * (glob)
  pretxnclose-hookarg: CLIENTEXTENSION_ext1 - 4.2.1337
  pretxnclose-hookarg: CLIENTEXTENSION_ext2 - unknown
  pretxnclose-hookarg: CLIENTEXTENSION_rebase - hg-* (glob)
  pretxnclose-hookarg: CLIENTEXTENSION_share - hg-* (glob)

#else

  $ hg push
  pushing to $TESTTMP/serverrepo
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  pretxnchangegroup-hookarg: CLIENTCONFIG_hgversion - * (glob)
  pretxnchangegroup-hookarg: CLIENTEXTENSION_configexpress - * (glob)
  pretxnchangegroup-hookarg: CLIENTEXTENSION_ext1 - 4.2.1337
  pretxnchangegroup-hookarg: CLIENTEXTENSION_ext2 - unknown
  pretxnchangegroup-hookarg: CLIENTEXTENSION_rebase - hg-* (glob)
  pretxnchangegroup-hookarg: CLIENTEXTENSION_share - hg-* (glob)
  pretxnclose-hookarg: CLIENTCONFIG_hgversion - * (glob)
  pretxnclose-hookarg: CLIENTEXTENSION_configexpress - * (glob)
  pretxnclose-hookarg: CLIENTEXTENSION_ext1 - 4.2.1337
  pretxnclose-hookarg: CLIENTEXTENSION_ext2 - unknown
  pretxnclose-hookarg: CLIENTEXTENSION_rebase - hg-* (glob)
  pretxnclose-hookarg: CLIENTEXTENSION_share - hg-* (glob)

#endif

  $ cd ..

  $ cd client-multiple-deficiencies
  $ hg pull
  pulling from $TESTTMP/serverrepo
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  new changesets c16e6831ba74 (?)
  (run 'hg update' to get a working copy)
  $ hg update
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ echo d > d
  $ hg add d
  $ hg commit -m D0

#if hg42

  $ hg push
  pushing to $TESTTMP/serverrepo
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  pretxnchangegroup-hookarg: CLIENTCONFIG_hgversion - * (glob)
  pretxnchangegroup-hookarg: CLIENTEXTENSION_configexpress - * (glob)
  pretxnchangegroup-hookarg: CLIENTEXTENSION_ext1 - 4.2.1337
  pretxnchangegroup-hookarg: CLIENTEXTENSION_ext2 - unknown
  pretxnchangegroup-hookarg: CLIENTEXTENSION_rebase - hg-* (glob)
  pretxnchangegroup-hookarg: CLIENTEXTENSION_share - hg-* (glob)
  pretxnclose-hookarg: CLIENTCONFIG_hgversion - * (glob)
  pretxnclose-hookarg: CLIENTEXTENSION_configexpress - * (glob)
  pretxnclose-hookarg: CLIENTEXTENSION_ext1 - 4.2.1337
  pretxnclose-hookarg: CLIENTEXTENSION_ext2 - unknown
  pretxnclose-hookarg: CLIENTEXTENSION_rebase - hg-* (glob)
  pretxnclose-hookarg: CLIENTEXTENSION_share - hg-* (glob)

#else

  $ hg push
  pushing to $TESTTMP/serverrepo
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  pretxnchangegroup-hookarg: CLIENTCONFIG_hgversion - * (glob)
  pretxnchangegroup-hookarg: CLIENTEXTENSION_configexpress - * (glob)
  pretxnchangegroup-hookarg: CLIENTEXTENSION_ext1 - 4.2.1337
  pretxnchangegroup-hookarg: CLIENTEXTENSION_ext2 - unknown
  pretxnchangegroup-hookarg: CLIENTEXTENSION_rebase - hg-* (glob)
  pretxnchangegroup-hookarg: CLIENTEXTENSION_share - hg-* (glob)
  pretxnclose-hookarg: CLIENTCONFIG_hgversion - * (glob)
  pretxnclose-hookarg: CLIENTEXTENSION_configexpress - * (glob)
  pretxnclose-hookarg: CLIENTEXTENSION_ext1 - 4.2.1337
  pretxnclose-hookarg: CLIENTEXTENSION_ext2 - unknown
  pretxnclose-hookarg: CLIENTEXTENSION_rebase - hg-* (glob)
  pretxnclose-hookarg: CLIENTEXTENSION_share - hg-* (glob)

#endif

  $ cd ..
