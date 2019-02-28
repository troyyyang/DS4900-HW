

```python
import pandas as pd
from sqlalchemy import create_engine
```

# Read in data


```python
engine = create_engine('postgresql://postgres:password@localhost:5432/ds4900')
```


```python
repo_query = 'select * from repos'
```


```python
repos = pd.read_sql(repo_query, engine)
```


```python
files_query = 'select * from files'
```


```python
files = pd.read_sql(files_query, engine)
```


```python
commits_query = 'select * from commits'
```


```python
commits = pd.read_sql(commits_query, engine)
```


```python
query = 'select * from github'
```


```python
github = pd.read_sql(query, engine)
```

# How many files, commits, and repos are there?


```python
print('There are '+ str(len(files)) +' files.')
```

    There are 40952 files.
    


```python
print('There are '+ str(len(commits)) +' commits.')
```

    There are 507180 commits.
    


```python
print('There are '+ str(len(repos)) +' repos.')
```

    There are 500 repos.
    

# How many unique authors and committers are there?


```python
print('There are '+ str(len(github['author_name'].unique())) +' unique authors.')
```

    There are 2032 unique authors.
    


```python
print('There are '+ str(len(github['committer_name'].unique())) +' unique committers.')
```

    There are 1718 unique committers.
    

# Truck factor


```python
authors_per_file = github.groupby('id')['author_name'].count()
```


```python
authors_per_path = pd.merge(pd.DataFrame(authors_per_file), files[['id', 'path']], on = 'id')[['path', 'author_name']]
```


```python
committers_per_file = github.groupby('id')['committer_name'].count()
```


```python
committers_per_path = pd.merge(pd.DataFrame(committers_per_file), files[['id', 'path']], on = 'id')[['path', 'committer_name']]
```

# Files with 2 or less authors


```python
authors_per_path[authors_per_path['author_name'] <= 2]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>path</th>
      <th>author_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>8</th>
      <td>i18n/fra/src/vs/workbench/parts/files/browser/...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>12</th>
      <td>test/ClangModules/bad-deployment-target.swift</td>
      <td>2</td>
    </tr>
    <tr>
      <th>14</th>
      <td>tensorflow/contrib/ios_examples/camera/CameraE...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>15</th>
      <td>stdlib/public/README.txt</td>
      <td>1</td>
    </tr>
    <tr>
      <th>18</th>
      <td>test/SourceKit/ExtractComment/extract_comments...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>23</th>
      <td>i18n/esn/src/vs/base/node/zip.i18n.json</td>
      <td>2</td>
    </tr>
    <tr>
      <th>26</th>
      <td>test/SourceKit/Sema/sema_lazy_var.swift.response</td>
      <td>1</td>
    </tr>
    <tr>
      <th>43</th>
      <td>unittests/SwiftDemangle/CMakeLists.txt</td>
      <td>2</td>
    </tr>
    <tr>
      <th>47</th>
      <td>i18n/deu/src/vs/workbench/browser/actions/togg...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>59</th>
      <td>i18n/rus/src/vs/platform/message/common/messag...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>68</th>
      <td>test/Driver/Dependencies/Inputs/private/d.swift</td>
      <td>2</td>
    </tr>
    <tr>
      <th>76</th>
      <td>i18n/cht/src/vs/workbench/browser/actions/trig...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>85</th>
      <td>i18n/rus/src/vs/platform/actions/common/action...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>90</th>
      <td>tensorflow/examples/android/src/org/tensorflow...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>110</th>
      <td>i18n/chs/src/vs/workbench/browser/parts/status...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>111</th>
      <td>test/Inputs/resilient_struct.swift</td>
      <td>2</td>
    </tr>
    <tr>
      <th>130</th>
      <td>tools/SourceKit/tools/sourcekitd/lib/CMakeList...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>149</th>
      <td>i18n/fra/src/vs/workbench/parts/git/browser/vi...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>163</th>
      <td>i18n/deu/src/vs/workbench/parts/git/browser/vi...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>193</th>
      <td>src/vs/editor/contrib/zoneWidget/browser/media...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>208</th>
      <td>src/vs/base/node/stream.ts</td>
      <td>2</td>
    </tr>
    <tr>
      <th>215</th>
      <td>src/vs/workbench/parts/git/browser/media/plus-...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>218</th>
      <td>test/SourceKit/Indexing/index_big_array.swift</td>
      <td>1</td>
    </tr>
    <tr>
      <th>222</th>
      <td>i18n/rus/src/vs/workbench/parts/files/common/e...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>224</th>
      <td>src/renderers/shared/stack/reconciler/__tests_...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>225</th>
      <td>i18n/esn/src/vs/workbench/parts/extensions/ele...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>235</th>
      <td>extensions/shaderlab/OSSREADME.json</td>
      <td>1</td>
    </tr>
    <tr>
      <th>241</th>
      <td>i18n/ita/src/vs/workbench/parts/files/browser/...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>247</th>
      <td>src/vs/workbench/parts/files/browser/media/Add...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>251</th>
      <td>docs/js/es5-sham.min.js</td>
      <td>2</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>20759</th>
      <td>i18n/chs/src/vs/workbench/browser/parts/editor...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20761</th>
      <td>test/SourceKit/Indexing/Inputs/implicit-vis/a....</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20764</th>
      <td>i18n/cht/src/vs/workbench/parts/debug/electron...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20765</th>
      <td>extensions/make/package.json</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20780</th>
      <td>resources/win32/bin/code.sh</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20788</th>
      <td>test/SourceKit/Inputs/placeholders.swift</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20794</th>
      <td>stdlib/public/SDK/Intents/INIntegerResolutionR...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20815</th>
      <td>i18n/rus/src/vs/platform/jsonschemas/common/js...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20816</th>
      <td>i18n/kor/src/vs/editor/contrib/toggleWordWrap/...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20829</th>
      <td>validation-test/compiler_crashers_fixed/26864-...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20850</th>
      <td>i18n/ita/src/vs/workbench/api/node/extHostMess...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20852</th>
      <td>validation-test/IDE/crashers_fixed/extension-p...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20853</th>
      <td>extensions/scss/syntaxes/scss.json</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20862</th>
      <td>test/IRGen/Inputs/witness_table_multifile_2.swift</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20866</th>
      <td>src/vs/base/common/buildunit.json</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20873</th>
      <td>test/Serialization/conformance-multi-file.swift</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20875</th>
      <td>i18n/jpn/src/vs/workbench/parts/quickopen/brow...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20876</th>
      <td>nanopb.BUILD</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20879</th>
      <td>extensions/typescript/server/typescript/Copyri...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20886</th>
      <td>docs/img/external_2x.png</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20899</th>
      <td>i18n/deu/src/vs/workbench/parts/files/browser/...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20926</th>
      <td>validation-test/compiler_crashers_fixed/28299-...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20934</th>
      <td>src/renderers/dom/shared/devtools/ReactDOMNull...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20949</th>
      <td>i18n/ita/src/vs/workbench/services/request/nod...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20950</th>
      <td>apinotes/AudioToolbox.apinotes</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20951</th>
      <td>test/PlaygroundTransform/do.swift</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20952</th>
      <td>stdlib/public/runtime/ReflectionNative.cpp</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20953</th>
      <td>docs/css/main.css</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20954</th>
      <td>extensions/swift/syntaxes/swift.json</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20957</th>
      <td>i18n/deu/src/vs/workbench/parts/git/browser/gi...</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
<p>2689 rows × 2 columns</p>
</div>



# Files with 2 or less committers


```python
committers_per_path[committers_per_path['committer_name'] <= 2]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>path</th>
      <th>committer_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>8</th>
      <td>i18n/fra/src/vs/workbench/parts/files/browser/...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>12</th>
      <td>test/ClangModules/bad-deployment-target.swift</td>
      <td>2</td>
    </tr>
    <tr>
      <th>14</th>
      <td>tensorflow/contrib/ios_examples/camera/CameraE...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>15</th>
      <td>stdlib/public/README.txt</td>
      <td>1</td>
    </tr>
    <tr>
      <th>18</th>
      <td>test/SourceKit/ExtractComment/extract_comments...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>23</th>
      <td>i18n/esn/src/vs/base/node/zip.i18n.json</td>
      <td>2</td>
    </tr>
    <tr>
      <th>26</th>
      <td>test/SourceKit/Sema/sema_lazy_var.swift.response</td>
      <td>1</td>
    </tr>
    <tr>
      <th>43</th>
      <td>unittests/SwiftDemangle/CMakeLists.txt</td>
      <td>2</td>
    </tr>
    <tr>
      <th>47</th>
      <td>i18n/deu/src/vs/workbench/browser/actions/togg...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>59</th>
      <td>i18n/rus/src/vs/platform/message/common/messag...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>68</th>
      <td>test/Driver/Dependencies/Inputs/private/d.swift</td>
      <td>2</td>
    </tr>
    <tr>
      <th>76</th>
      <td>i18n/cht/src/vs/workbench/browser/actions/trig...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>85</th>
      <td>i18n/rus/src/vs/platform/actions/common/action...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>90</th>
      <td>tensorflow/examples/android/src/org/tensorflow...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>110</th>
      <td>i18n/chs/src/vs/workbench/browser/parts/status...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>111</th>
      <td>test/Inputs/resilient_struct.swift</td>
      <td>2</td>
    </tr>
    <tr>
      <th>130</th>
      <td>tools/SourceKit/tools/sourcekitd/lib/CMakeList...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>149</th>
      <td>i18n/fra/src/vs/workbench/parts/git/browser/vi...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>163</th>
      <td>i18n/deu/src/vs/workbench/parts/git/browser/vi...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>193</th>
      <td>src/vs/editor/contrib/zoneWidget/browser/media...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>208</th>
      <td>src/vs/base/node/stream.ts</td>
      <td>2</td>
    </tr>
    <tr>
      <th>215</th>
      <td>src/vs/workbench/parts/git/browser/media/plus-...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>218</th>
      <td>test/SourceKit/Indexing/index_big_array.swift</td>
      <td>1</td>
    </tr>
    <tr>
      <th>222</th>
      <td>i18n/rus/src/vs/workbench/parts/files/common/e...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>224</th>
      <td>src/renderers/shared/stack/reconciler/__tests_...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>225</th>
      <td>i18n/esn/src/vs/workbench/parts/extensions/ele...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>235</th>
      <td>extensions/shaderlab/OSSREADME.json</td>
      <td>1</td>
    </tr>
    <tr>
      <th>241</th>
      <td>i18n/ita/src/vs/workbench/parts/files/browser/...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>247</th>
      <td>src/vs/workbench/parts/files/browser/media/Add...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>251</th>
      <td>docs/js/es5-sham.min.js</td>
      <td>2</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>20759</th>
      <td>i18n/chs/src/vs/workbench/browser/parts/editor...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20761</th>
      <td>test/SourceKit/Indexing/Inputs/implicit-vis/a....</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20764</th>
      <td>i18n/cht/src/vs/workbench/parts/debug/electron...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20765</th>
      <td>extensions/make/package.json</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20780</th>
      <td>resources/win32/bin/code.sh</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20788</th>
      <td>test/SourceKit/Inputs/placeholders.swift</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20794</th>
      <td>stdlib/public/SDK/Intents/INIntegerResolutionR...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20815</th>
      <td>i18n/rus/src/vs/platform/jsonschemas/common/js...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20816</th>
      <td>i18n/kor/src/vs/editor/contrib/toggleWordWrap/...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20829</th>
      <td>validation-test/compiler_crashers_fixed/26864-...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20850</th>
      <td>i18n/ita/src/vs/workbench/api/node/extHostMess...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20852</th>
      <td>validation-test/IDE/crashers_fixed/extension-p...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20853</th>
      <td>extensions/scss/syntaxes/scss.json</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20862</th>
      <td>test/IRGen/Inputs/witness_table_multifile_2.swift</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20866</th>
      <td>src/vs/base/common/buildunit.json</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20873</th>
      <td>test/Serialization/conformance-multi-file.swift</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20875</th>
      <td>i18n/jpn/src/vs/workbench/parts/quickopen/brow...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20876</th>
      <td>nanopb.BUILD</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20879</th>
      <td>extensions/typescript/server/typescript/Copyri...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20886</th>
      <td>docs/img/external_2x.png</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20899</th>
      <td>i18n/deu/src/vs/workbench/parts/files/browser/...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20926</th>
      <td>validation-test/compiler_crashers_fixed/28299-...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20934</th>
      <td>src/renderers/dom/shared/devtools/ReactDOMNull...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20949</th>
      <td>i18n/ita/src/vs/workbench/services/request/nod...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20950</th>
      <td>apinotes/AudioToolbox.apinotes</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20951</th>
      <td>test/PlaygroundTransform/do.swift</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20952</th>
      <td>stdlib/public/runtime/ReflectionNative.cpp</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20953</th>
      <td>docs/css/main.css</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20954</th>
      <td>extensions/swift/syntaxes/swift.json</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20957</th>
      <td>i18n/deu/src/vs/workbench/parts/git/browser/gi...</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
<p>2689 rows × 2 columns</p>
</div>


