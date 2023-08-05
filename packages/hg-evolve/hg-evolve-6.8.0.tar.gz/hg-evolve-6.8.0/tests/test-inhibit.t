  $ cat >> $HGRCPATH <<EOF
  > [ui]
  > logtemplate = {rev}:{node|short} {desc}\n
  > [experimental]
  > prunestrip=True
  > evolution=createmarkers
  > [extensions]
  > rebase=
  > strip=
  > EOF
  $ echo "evolve=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/" >> $HGRCPATH
  $ echo "directaccess=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/hack/directaccess.py" >> $HGRCPATH
  $ echo "inhibit=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/hack/inhibit.py" >> $HGRCPATH
  $ mkcommit() {
  >    echo "$1" > "$1"
  >    hg add "$1"
  >    hg ci -m "add $1"
  > }

  $ hg init inhibit
  $ cd inhibit
  $ mkcommit cA
  $ mkcommit cB
  $ mkcommit cC
  $ mkcommit cD
  $ hg up 'desc(cA)'
  0 files updated, 0 files merged, 3 files removed, 0 files unresolved
  $ mkcommit cE
  created new head
  $ mkcommit cG
  $ mkcommit cH
  $ mkcommit cJ
  $ hg log -G
  @  7:18214586bf78 add cJ
  |
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  | o  3:2db36d8066ff add cD
  | |
  | o  2:7df62a38b9bf add cC
  | |
  | o  1:02bcbc3f6e56 add cB
  |/
  o  0:54ccbc537fc2 add cA
  

plain prune

  $ hg strip 1::
  3 changesets pruned
  $ hg log -G
  @  7:18214586bf78 add cJ
  |
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  
  $ hg debugobsinhibit --hidden 1::
  $ hg log -G
  @  7:18214586bf78 add cJ
  |
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  | o  3:2db36d8066ff add cD
  | |
  | o  2:7df62a38b9bf add cC
  | |
  | o  1:02bcbc3f6e56 add cB
  |/
  o  0:54ccbc537fc2 add cA
  
  $ hg strip --hidden 1::
  3 changesets pruned
  $ hg log -G
  @  7:18214586bf78 add cJ
  |
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  

after amend

  $ echo babar > cJ
  $ hg commit --amend
  $ hg log -G
  @  8:55c73a90e4b4 add cJ
  |
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  
  $ hg debugobsinhibit --hidden 18214586bf78
  $ hg log -G
  @  8:55c73a90e4b4 add cJ
  |
  | o  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  

and no divergence

  $ hg summary
  parent: 8:55c73a90e4b4 tip
   add cJ
  branch: default
  commit: (clean)
  update: 1 new changesets, 2 branch heads (merge)
  phases: 6 draft

check public revision got cleared
(when adding the second inhibitor, the first one is removed because it is public)

  $ wc -m .hg/store/obsinhibit | sed -e 's/^[ \t]*//'
  20 .hg/store/obsinhibit
  $ hg strip 7
  1 changesets pruned
  $ hg debugobsinhibit --hidden 18214586bf78
  $ wc -m .hg/store/obsinhibit | sed -e 's/^[ \t]*//'
  20 .hg/store/obsinhibit
  $ hg log -G
  @  8:55c73a90e4b4 add cJ
  |
  | o  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  
  $ hg phase --public 7
  1 new phase-divergent changesets
  $ hg strip 8
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  working directory now at cf5c4f4554ce
  1 changesets pruned
  $ hg log -G
  o  7:18214586bf78 add cJ
  |
  @  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  
  $ hg debugobsinhibit --hidden 55c73a90e4b4
  $ wc -m .hg/store/obsinhibit | sed -e 's/^[ \t]*//'
  20 .hg/store/obsinhibit
  $ hg log -G
  o  8:55c73a90e4b4 add cJ
  |
  | o  7:18214586bf78 add cJ
  |/
  @  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  
Update should inhibit all related unstable commits

  $ hg update 2 --hidden
  2 files updated, 0 files merged, 3 files removed, 0 files unresolved
  $ hg log -G
  o  8:55c73a90e4b4 add cJ
  |
  | o  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  | @  2:7df62a38b9bf add cC
  | |
  | o  1:02bcbc3f6e56 add cB
  |/
  o  0:54ccbc537fc2 add cA
  

  $ hg update 8
  4 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ hg log -G
  @  8:55c73a90e4b4 add cJ
  |
  | o  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  | o  2:7df62a38b9bf add cC
  | |
  | o  1:02bcbc3f6e56 add cB
  |/
  o  0:54ccbc537fc2 add cA
  
  $ hg strip --hidden 1::
  3 changesets pruned
  $ hg log -G
  @  8:55c73a90e4b4 add cJ
  |
  | o  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  

Bookmark should inhibit all related unstable commits
  $ hg bookmark -r 2 book1  --hidden
  $ hg log -G
  @  8:55c73a90e4b4 add cJ
  |
  | o  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  | o  2:7df62a38b9bf add cC
  | |
  | o  1:02bcbc3f6e56 add cB
  |/
  o  0:54ccbc537fc2 add cA
  

Removing a bookmark with bookmark -D should prune the changes underneath
that are not reachable from another bookmark or head

  $ hg bookmark -r 1 book2
  $ hg bookmark -D book1  --config experimental.evolution=createmarkers #--config to make sure prune is not registered as a command.
  bookmark 'book1' deleted
  1 changesets pruned
  $ hg log -G
  @  8:55c73a90e4b4 add cJ
  |
  | o  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  | o  1:02bcbc3f6e56 add cB
  |/
  o  0:54ccbc537fc2 add cA
  
  $ hg bookmark -D book2
  bookmark 'book2' deleted
  1 changesets pruned
  $ hg log -G
  @  8:55c73a90e4b4 add cJ
  |
  | o  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  
Test edge cases of bookmark -D
  $ hg book -D book2 -m hello
  abort: Cannot use both -m and -D
  [255]

  $ hg book -Draster-fix
  abort: Error, please check your command
  (make sure to put a space between -D and your bookmark name)
  [255]

Test that direct access make changesets visible

  $ hg export 2db36d8066ff 02bcbc3f6e56
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 2db36d8066ff50e8be3d3e6c2da1ebc0a8381d82
  # Parent  7df62a38b9bf9daf968de235043ba88a8ef43393
  add cD
  
  diff -r 7df62a38b9bf -r 2db36d8066ff cD
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/cD	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +cD
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 02bcbc3f6e56fb2928efec2c6e24472720bf5511
  # Parent  54ccbc537fc2d6845a5d61337c1cfb80d1d2815e
  add cB
  
  diff -r 54ccbc537fc2 -r 02bcbc3f6e56 cB
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/cB	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +cB

But only with hash

  $ hg export 2db36d8066ff::
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 2db36d8066ff50e8be3d3e6c2da1ebc0a8381d82
  # Parent  7df62a38b9bf9daf968de235043ba88a8ef43393
  add cD
  
  diff -r 7df62a38b9bf -r 2db36d8066ff cD
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/cD	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +cD

  $ hg export 1 3
  abort: hidden revision '1'!
  (use --hidden to access hidden revisions; pruned)
  [255]


Test directaccess in a larger revset

  $ hg log -r '. + .^ + 2db36d8066ff' -T '{node|short}\n'
  55c73a90e4b4
  cf5c4f4554ce
  2db36d8066ff

Test directaccess only takes hashes

  $ HOOKPATH=$TESTTMP/printexplicitaccess.py
  $ cat >> $HOOKPATH <<EOF
  > def hook(ui, repo, **kwds):
  >     for i in sorted(repo._explicitaccess):
  >         ui.write('directaccess: %s\n' % i)
  > EOF

  $ hg log -r 1 -r 2 -r 2db36d8066f -T '{rev}\n' --config hooks.post-log=python:$HOOKPATH:hook
  1
  2
  3
  directaccess: 3

With severals hidden sha, rebase of one hidden stack onto another one:
  $ hg update -C 0
  0 files updated, 0 files merged, 4 files removed, 0 files unresolved
  $ mkcommit cK
  created new head
  $ mkcommit cL
  $ hg update -C 8
  4 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ hg log -G
  o  10:53a94305e133 add cL
  |
  o  9:ad78ff7d621f add cK
  |
  | @  8:55c73a90e4b4 add cJ
  | |
  | | o  7:18214586bf78 add cJ
  | |/
  | o  6:cf5c4f4554ce add cH
  | |
  | o  5:5419eb264a33 add cG
  | |
  | o  4:98065434e5c6 add cE
  |/
  o  0:54ccbc537fc2 add cA
  
  $ hg strip --hidden 9:
  2 changesets pruned
  $ hg log -G
  @  8:55c73a90e4b4 add cJ
  |
  | o  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  
  $ hg rebase -s 9 -d 3 
  abort: hidden revision '9'!
  (use --hidden to access hidden revisions; pruned)
  [255]
  $ hg rebase -r ad78ff7d621f -r 53a94305e133 -d  2db36d8066ff --config experimental.rebaseskipobsolete=0
  Warning: accessing hidden changesets ad78ff7d621f,53a94305e133 for write operation
  Warning: accessing hidden changesets 2db36d8066ff for write operation
  rebasing 9:ad78ff7d621f "add cK"
  rebasing 10:53a94305e133 "add cL" (tip)
  $ hg log -G
  o  12:2f7b7704d714 add cL
  |
  o  11:fe1634cbe235 add cK
  |
  | @  8:55c73a90e4b4 add cJ
  | |
  | | o  7:18214586bf78 add cJ
  | |/
  | o  6:cf5c4f4554ce add cH
  | |
  | o  5:5419eb264a33 add cG
  | |
  | o  4:98065434e5c6 add cE
  | |
  o |  3:2db36d8066ff add cD
  | |
  o |  2:7df62a38b9bf add cC
  | |
  o |  1:02bcbc3f6e56 add cB
  |/
  o  0:54ccbc537fc2 add cA
  

Check that amending in the middle of a stack does not show obsolete revs
Since we are doing operation in the middle of the stack we cannot just
have createmarkers as we are creating instability

  $ cat >> $HGRCPATH <<EOF
  > [experimental]
  > evolution=all
  > EOF

  $ hg strip --hidden 1::
  5 changesets pruned
  $ hg log -G
  @  8:55c73a90e4b4 add cJ
  |
  | o  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  
  $ hg up 7
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ mkcommit cL
  $ mkcommit cM
  $ mkcommit cN
  $ hg log -G
  @  15:a438c045eb37 add cN
  |
  o  14:2d66e189f5b5 add cM
  |
  o  13:d66ccb8c5871 add cL
  |
  | o  8:55c73a90e4b4 add cJ
  | |
  o |  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  
  $ hg up 14
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo "mmm" >> cM
  $ hg amend
  $ hg log -G
  @  16:210589181b14 add cM
  |
  | o  15:a438c045eb37 add cN
  | |
  | o  14:2d66e189f5b5 add cM
  |/
  o  13:d66ccb8c5871 add cL
  |
  | o  8:55c73a90e4b4 add cJ
  | |
  o |  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  
Check that rebasing a commit twice makes the commit visible again

  $ hg rebase -d 16 -r 15 --keep
  rebasing 15:a438c045eb37 "add cN"
  $ hg log -r 13:: -G
  o  17:104eed5354c7 add cN
  |
  @  16:210589181b14 add cM
  |
  | o  15:a438c045eb37 add cN
  | |
  | o  14:2d66e189f5b5 add cM
  |/
  o  13:d66ccb8c5871 add cL
  |
  ~
  $ hg strip -r 210589181b14
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  working directory now at d66ccb8c5871
  2 changesets pruned

Using a hash prefix solely made of digits should work
  $ hg update 210589181
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg rebase -d 16 -r 15 --keep
  rebasing 15:a438c045eb37 "add cN"
  $ hg log -r 13:: -G
  o  17:104eed5354c7 add cN
  |
  @  16:210589181b14 add cM
  |
  | o  15:a438c045eb37 add cN
  | |
  | o  14:2d66e189f5b5 add cM
  |/
  o  13:d66ccb8c5871 add cL
  |
  ~

Test prunestrip

  $ hg book foo -r 104eed5354c7
  $ hg strip -r 210589181b14
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  working directory now at d66ccb8c5871
  2 changesets pruned
  $ hg log -r 13:: -G -T '{rev}:{node|short} {desc|firstline} {bookmarks}\n'
  o  15:a438c045eb37 add cN
  |
  o  14:2d66e189f5b5 add cM
  |
  @  13:d66ccb8c5871 add cL foo
  |
  ~

Check that --hidden used with inhibit does not hide every obsolete commit
We show the log before and after a log -G --hidden, they should be the same
  $ hg log -G
  o  15:a438c045eb37 add cN
  |
  o  14:2d66e189f5b5 add cM
  |
  @  13:d66ccb8c5871 add cL
  |
  | o  8:55c73a90e4b4 add cJ
  | |
  o |  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  
  $ hg log -G --hidden
  x  17:104eed5354c7 add cN
  |
  x  16:210589181b14 add cM
  |
  | o  15:a438c045eb37 add cN
  | |
  | o  14:2d66e189f5b5 add cM
  |/
  @  13:d66ccb8c5871 add cL
  |
  | x  12:2f7b7704d714 add cL
  | |
  | x  11:fe1634cbe235 add cK
  | |
  | | x  10:53a94305e133 add cL
  | | |
  | | x  9:ad78ff7d621f add cK
  | | |
  | | | o  8:55c73a90e4b4 add cJ
  | | | |
  o-----+  7:18214586bf78 add cJ
   / / /
  | | o  6:cf5c4f4554ce add cH
  | | |
  | | o  5:5419eb264a33 add cG
  | | |
  | | o  4:98065434e5c6 add cE
  | |/
  x |  3:2db36d8066ff add cD
  | |
  x |  2:7df62a38b9bf add cC
  | |
  x |  1:02bcbc3f6e56 add cB
  |/
  o  0:54ccbc537fc2 add cA
  

  $ hg log -G
  o  15:a438c045eb37 add cN
  |
  o  14:2d66e189f5b5 add cM
  |
  @  13:d66ccb8c5871 add cL
  |
  | o  8:55c73a90e4b4 add cJ
  | |
  o |  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  
 
check that pruning and inhibited node does not confuse anything

  $ hg up --hidden 210589181b14
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg strip --bundle 210589181b14
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  saved backup bundle to $TESTTMP/inhibit/.hg/strip-backup/210589181b14-e09c7b88-backup.hg (glob)
  $ hg unbundle .hg/strip-backup/210589181b14-e09c7b88-backup.hg # restore state
  adding changesets
  adding manifests
  adding file changes
  added 2 changesets with 1 changes to 2 files (+1 heads)
  3 new obsolescence markers
  obsoleted 1 changesets
  new changesets 210589181b14
  (run 'hg heads .' to see heads, 'hg merge' to merge)

 Only allow direct access and check that evolve works like before
(also disable evolve commands to avoid hint about using evolve)
  $ cat >> $HGRCPATH <<EOF
  > [extensions]
  > inhibit=!
  > [experimental]
  > evolution=createmarkers
  > EOF

  $ hg up 14
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory parent is obsolete! (2d66e189f5b5)
  $ cat >> $HGRCPATH <<EOF
  > [experimental]
  > evolution=all
  > EOF
  $ echo "CM" > cM
  $ hg amend
  $ hg log -G
  @  18:721c3c279519 add cM
  |
  | o  15:a438c045eb37 add cN
  | |
  | x  14:2d66e189f5b5 add cM
  |/
  o  13:d66ccb8c5871 add cL
  |
  o  7:18214586bf78 add cJ
  |
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  
  $ cat >> $HGRCPATH <<EOF
  > [extensions]
  > EOF
  $ echo "inhibit=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/hack/inhibit.py" >> $HGRCPATH

Empty commit
  $ hg amend
  nothing changed
  [1]

Check that the behavior of rebase with obsolescence markers is maintained
despite inhibit

  $ hg up a438c045eb37
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg rebase -r 14:: -d 18 --config experimental.rebaseskipobsolete=True
  note: not rebasing 14:2d66e189f5b5 "add cM", already in destination as 18:721c3c279519 "add cM" (tip)
  rebasing 15:a438c045eb37 "add cN"
  $ hg up -q 2d66e189f5b5 # To inhibit it as the rest of test depends on it
  $ hg up -q 18

Directaccess should load after some extensions precised in the conf
With no extension specified:

  $ cat >$TESTTMP/test_extension.py  << EOF
  > from mercurial import extensions
  > def uisetup(ui):
  >   print extensions._order
  > EOF
  $ cat >> $HGRCPATH << EOF
  > [extensions]
  > testextension=$TESTTMP/test_extension.py
  > EOF
  $ hg id
  ['rebase', 'strip', 'evolve', 'directaccess', 'inhibit', 'testextension']
  721c3c279519

With test_extension specified:
  $ cat >> $HGRCPATH << EOF
  > [directaccess]
  > loadsafter=testextension
  > EOF
  $ hg id
  ['rebase', 'strip', 'evolve', 'inhibit', 'testextension', 'directaccess']
  721c3c279519

Inhibit should not work without directaccess
  $ cat >> $HGRCPATH <<EOF
  > [extensions]
  > directaccess=!
  > testextension=!
  > EOF
  $ hg up .
  cannot use inhibit without the direct access extension
  (please enable it or inhibit won't work)
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ echo "directaccess=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/hack/directaccess.py" >> $HGRCPATH
  $ cd ..

hg push should not allow directaccess unless forced with --hidden
We copy the inhibhit repo to inhibit2 and make some changes to push to inhibit

  $ cp -r inhibit inhibit2
  $ pwd=$(pwd)
  $ cd inhibit
  $ mkcommit pk
  created new head
  $ hg id
  003a4735afde tip
  $ echo "OO" > pk
  $ hg amend
  $ hg id
  71eb4f100663 tip

Hidden commits cannot be pushed without --hidden
  $ hg push -r 003a4735afde $pwd/inhibit2
  pushing to $TESTTMP/inhibit2
  abort: hidden revision '003a4735afde'!
  (use --hidden to access hidden revisions; successor: 71eb4f100663)
  [255]

Visible commits can still be pushed
  $ hg push -fr 71eb4f100663 $pwd/inhibit2
  pushing to $TESTTMP/inhibit2
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files (+1 heads)
  1 new obsolescence markers

Create a stack (obsolete with successor in dest) -> (not obsolete) and rebase
it. We expect to not see the stack at the end of the rebase.
  $ hg log -G  -r "003a4735afde::"
  x  20:003a4735afde add pk
  |
  ~
  $ hg log -G
  @  21:71eb4f100663 add pk
  |
  | o  19:46cb6daad392 add cN
  |/
  o  18:721c3c279519 add cM
  |
  | o  16:210589181b14 add cM
  |/
  | o  14:2d66e189f5b5 add cM
  |/
  o  13:d66ccb8c5871 add cL
  |
  | o  8:55c73a90e4b4 add cJ
  | |
  o |  7:18214586bf78 add cJ
  |/
  o  6:cf5c4f4554ce add cH
  |
  o  5:5419eb264a33 add cG
  |
  o  4:98065434e5c6 add cE
  |
  o  0:54ccbc537fc2 add cA
  
  $ hg up -C 46cb6daad392
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ mkcommit Dk
  $ hg prune 46cb6daad392 -s 71eb4f100663
  1 changesets pruned
  $ hg rebase -s 46cb6daad392 -d 71eb4f100663 --config experimental.rebaseskipobsolete=True
  note: not rebasing 19:46cb6daad392 "add cN", already in destination as 21:71eb4f100663 "add pk"
  rebasing 22:7ad60e760c7b "add Dk" (tip)
  $ hg log -G  -r "71eb4f100663::"
  @  23:1192fa9fbc68 add Dk
  |
  o  21:71eb4f100663 add pk
  |
  ~

Create a stack (obsolete with succ in dest) -> (not obsolete) -> (not obsolete).
Rebase the first two revs of the stack onto dest, we expect to see one new
revision on the destination and everything visible.
  $ hg up 71eb4f100663
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ mkcommit Dl
  created new head
  $ mkcommit Dp
  $ mkcommit Do
  $ hg log -G -r "71eb4f100663::"
  @  26:b517facce1ef add Do
  |
  o  25:c5a47ab27c2e add Dp
  |
  o  24:8c1c2edbaf1b add Dl
  |
  | o  23:1192fa9fbc68 add Dk
  |/
  o  21:71eb4f100663 add pk
  |
  ~
  $ hg prune 8c1c2edbaf1b -s 1192fa9fbc68
  1 changesets pruned
  $ hg up 71eb4f100663
  0 files updated, 0 files merged, 3 files removed, 0 files unresolved
  $ hg rebase -r "8c1c2edbaf1b + c5a47ab27c2e" --keep -d 1192fa9fbc68 --config experimental.rebaseskipobsolete=True
  note: not rebasing 24:8c1c2edbaf1b "add Dl", already in destination as 23:1192fa9fbc68 "add Dk"
  rebasing 25:c5a47ab27c2e "add Dp"
  $ hg log -G  -r "71eb4f100663::"
  o  27:7d8affb1f604 add Dp
  |
  | o  26:b517facce1ef add Do
  | |
  | o  25:c5a47ab27c2e add Dp
  | |
  | o  24:8c1c2edbaf1b add Dl
  | |
  o |  23:1192fa9fbc68 add Dk
  |/
  @  21:71eb4f100663 add pk
  |
  ~

Rebase the same stack in full on the destination, we expect it to disappear
and only see the top revision added to destination. We don\'t expect 29 to be
skipped as we used --keep before.
  $ hg rebase -s 8c1c2edbaf1b -d 1192fa9fbc68 --config experimental.rebaseskipobsolete=True
  note: not rebasing 24:8c1c2edbaf1b "add Dl", already in destination as 23:1192fa9fbc68 "add Dk"
  rebasing 25:c5a47ab27c2e "add Dp"
  rebasing 26:b517facce1ef "add Do"
  $ hg log -G  -r "71eb4f100663::"
  o  28:1d43fff9e26f add Do
  |
  o  27:7d8affb1f604 add Dp
  |
  o  23:1192fa9fbc68 add Dk
  |
  @  21:71eb4f100663 add pk
  |
  ~

Pulling from a inhibit repo to a non-inhibit repo should work

  $ cd ..
  $ hg clone -q inhibit not-inhibit
  $ cat >> not-inhibit/.hg/hgrc <<EOF
  > [extensions]
  > inhibit=!
  > directaccess=!
  > evolve=!
  > EOF
  $ cd not-inhibit
  $ hg book -d foo
  $ hg pull
  pulling from $TESTTMP/inhibit (glob)
  searching for changes
  no changes found
  adding remote bookmark foo

Test that bookmark -D can take multiple branch names
  $ cd ../inhibit
  $ hg bookmark book2 book1 book3
  $ touch foo && hg add foo && hg ci -m "add foo"
  created new head
  $ hg up book1
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  (activating bookmark book1)
  $ hg bookmark -D book2 book3
  bookmark 'book2' deleted
  bookmark 'book3' deleted
  1 changesets pruned
