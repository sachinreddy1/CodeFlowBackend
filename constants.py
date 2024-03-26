SINGLE_GENERATION_TEMPLATE="""
You take source code and generates a flowchart in Mermaid syntax. Only reply with the Mermaid syntax, starting with 'graph LR'.

An example of the correct input/output would be:

Example 1)
Input:

<repository index="1">
<repository_source>
sachinreddy1/github-content-api/main
</repository_source>
<document index="1">
<source>
github-content-api/src/main/kotlin/com/sachinreddy/githubcontentapi/GithubContentApiApplication.kt
</source>
<document_content>
package com.sachinreddy.githubcontentapi

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class GithubContentApiApplication

fun main(args: Array<String>) {{
        runApplication<GithubContentApiApplication>(*args)
}}

</document_content>
</document>
<document index="2">
<source>
github-content-api/src/main/kotlin/com/sachinreddy/githubcontentapi/config/AppConfig.kt
</source>
<document_content>
package com.sachinreddy.githubcontentapi.config

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.web.reactive.function.client.WebClient

@Configuration
class AppConfig {{
    @Bean
    fun webClient(): WebClient = WebClient.create()
}}

</document_content>
</document>
<document index="3">
<source>
github-content-api/src/main/kotlin/com/sachinreddy/githubcontentapi/controller/GitHubContentController.kt
</source>
<document_content>
package com.sachinreddy.githubcontentapi.controller

import com.sachinreddy.githubcontentapi.model.GitHubContentRequest
import com.sachinreddy.githubcontentapi.model.GitHubTreeResponse
import com.sachinreddy.githubcontentapi.service.GitHubContentService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("v1/github/content")
class GitHubContentController @Autowired constructor(
    private val gitHubContentService: GitHubContentService
){{
    @GetMapping
    @ResponseStatus(HttpStatus.OK)
    fun getContent(
        @RequestBody gitHubContentRequest: GitHubContentRequest
    ): String {{
        return gitHubContentService.getContent(gitHubContentRequest)
    }}
}}
</document_content>
</document>
<document index="4">
<source>
github-content-api/src/main/kotlin/com/sachinreddy/githubcontentapi/controller/HelloWorldController.kt
</source>
<document_content>
package com.sachinreddy.githubcontentapi.controller

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("hello")
class HelloWorldController {{
    @GetMapping
    fun helloWorld(): String = "Hello world."
}}
</document_content>
</document>
<document index="5">
<source>
github-content-api/src/main/kotlin/com/sachinreddy/githubcontentapi/model/GitHubBlobResponse.kt
</source>
<document_content>
package com.sachinreddy.githubcontentapi.model

import com.fasterxml.jackson.annotation.JsonProperty

data class GitHubBlobResponse(
    @JsonProperty("content")
    val content: String?
)
</document_content>
</document>
<document index="6">
<source>
github-content-api/src/main/kotlin/com/sachinreddy/githubcontentapi/model/GitHubContentRequest.kt
</source>
<document_content>
package com.sachinreddy.githubcontentapi.model

import com.fasterxml.jackson.annotation.JsonProperty

data class GitHubContentRequest(
    @JsonProperty("url")
    val url: String,

    @JsonProperty("branch")
    val branch: String
)
</document_content>
</document>
<document index="7">
<source>
github-content-api/src/main/kotlin/com/sachinreddy/githubcontentapi/model/GitHubTreeFile.kt
</source>
<document_content>
package com.sachinreddy.githubcontentapi.model

import com.fasterxml.jackson.annotation.JsonProperty

data class GitHubTreeFile(
    @JsonProperty("path")
    val path: String,

    @JsonProperty("url")
    val url: String
)
</document_content>
</document>
<document index="8">
<source>
github-content-api/src/main/kotlin/com/sachinreddy/githubcontentapi/model/GitHubTreeResponse.kt
</source>
<document_content>
package com.sachinreddy.githubcontentapi.model

import com.fasterxml.jackson.annotation.JsonProperty

data class GitHubTreeResponse(
    @JsonProperty("tree")
    val tree: List<GitHubTreeFile>
)
</document_content>
</document>
<document index="9">
<source>
github-content-api/src/main/kotlin/com/sachinreddy/githubcontentapi/service/GitHubContentService.kt
</source>
<document_content>
package com.sachinreddy.githubcontentapi.service

import com.sachinreddy.githubcontentapi.model.GitHubBlobResponse
import com.sachinreddy.githubcontentapi.model.GitHubContentRequest
import com.sachinreddy.githubcontentapi.model.GitHubTreeResponse
import org.apache.tomcat.util.codec.binary.Base64.decodeBase64
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service
import org.springframework.web.reactive.function.client.WebClient
import java.util.*

@Service
class GitHubContentService @Autowired constructor(
    val webClient: WebClient
) {{
    @Value("\${{gitHub.url}}")
    private val treeUrl: String? = null

    @Value("\${{gitHub.auth}}")
    private val auth: String? = null

    fun getContent(gitHubContentRequest: GitHubContentRequest): String {{
        val url = gitHubContentRequest.url
        val branch = gitHubContentRequest.branch

        val urlComponents = url.split('/')

        if (!urlComponents.contains("github.com")) {{
            throw Exception("URL is invalid.")
        }}

        val owner = urlComponents[urlComponents.size - 2]
        val repository = urlComponents[urlComponents.size - 1]

        if (repository.endsWith(".git")) {{
            throw Exception("URL is invalid.")
        }}

        val treeURL = treeUrl!!.format(owner, repository, branch)

        return getContentString(getGitHubTree(treeURL))
    }}

    private fun getContentString(gitHubTreeResponse: GitHubTreeResponse): String {{
        var ret = "<documents>\n"
        var index = 1

        gitHubTreeResponse.tree.forEach {{
            val blob = getGitHubBlob(it.url)

            try {{
                blob.content?.let {{ blobContent ->
                    ret += "<document index=\"${{index}}\">\n"
                    ret += "<source>\n"
                    ret += "${{it.path}}\n"
                    ret += "</source>\n"
                    ret += "<document_content>\n"
                    ret += "${{decodeBase64(blobContent.replace("\n", ""))}}\n"
                    ret += "</document_content>\n"
                    ret += "</document>\n"

                    index += 1
                }}
            }} catch (e: Exception) {{

            }}
        }}

        ret += "</documents>\n"

        return ret
    }}

    private fun decodeBase64(base64String: String): String {{
        val decodedBytes = Base64.getDecoder().decode(base64String)
        return String(decodedBytes)
    }}

    private fun getGitHubTree(url: String): GitHubTreeResponse {{
        val response = webClient.get()
                .uri(url)
                .header("Authorization", auth)
                .retrieve()
                .bodyToMono(GitHubTreeResponse::class.java)

        return response.block()!!
    }}

    private fun getGitHubBlob(url: String): GitHubBlobResponse {{
        val response = webClient.get()
                .uri(url)
                .header("Authorization", auth)
                .retrieve()
                .bodyToMono(GitHubBlobResponse::class.java)

        return response.block()!!
    }}
}}
</document_content>
</document>
<document index="10">
<source>
github-content-api/src/main/resources/application.yml
</source>
<document_content>
gitHub:
  url: "https://api.github.com/repos/%s/%s/git/trees/%s?recursive=true"
  auth:
</document_content>
</document>
<document index="11">
<source>
github-content-api/src/test/kotlin/com/sachinreddy/githubcontentapi/GithubContentApiApplicationTests.kt
</source>
<document_content>
package com.sachinreddy.githubcontentapi

import org.junit.jupiter.api.Test
import org.springframework.boot.test.context.SpringBootTest

@SpringBootTest
class GithubContentApiApplicationTests {{

        @Test
        fun contextLoads() {{
        }}

}}

</document_content>
</document>
</repository>

Output:

graph LR
    A[GithubContentApiApplication.kt\n\n Description: Main class of the Springboot application.] --> B[GitHubContentController.kt\n\n Access Path - GET: /v1/github/content\n Description: Entry point for the GitHub Content Service.]
    A --> C[HelloWorldController.kt\n\n Access Path - GET: /hello\n Description: Controller, GET path returns Hello world.]
    B --> D[GitHubContentService.kt\n\n External API call: https://api.github.com\n Description: Returns a concatenated string of all the files in the GitHub repository. Calls the GitHub API to get file contents.]

Example 2)
Input:

<repository index="1">
<repository_source>
sachinreddy1/CodeFlowUI/main
</repository_source>
<document index="1">
<source>
src/index.js
</source>
<document_content>
import React from 'react';
import ReactDOM from 'react-dom/client';
import './css/App.css';
import App from './ui/App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

</document_content>
</document>
<document index="2">
<source>
src/reportWebVitals.js
</source>
<document_content>
const reportWebVitals = onPerfEntry => {{
  if (onPerfEntry && onPerfEntry instanceof Function) {{
    import('web-vitals').then(({{ getCLS, getFID, getFCP, getLCP, getTTFB }}) => {{
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    }});
  }}
}};

export default reportWebVitals;

</document_content>
</document>
<document index="3">
<source>
src/test/App.test.js
</source>
<document_content>
import {{ render, screen }} from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {{
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
}});

</document_content>
</document>
<document index="4">
<source>
src/test/setupTests.js
</source>
<document_content>
// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

</document_content>
</document>
<document index="5">
<source>
src/ui/AddLinkButton.js
</source>
<document_content>
import React from "react";
import IconButton from '@mui/material/IconButton';
import AddCircleIcon from '@mui/icons-material/AddCircle';

function AddLinkButton(props) {{
    return (
        <IconButton
            aria-label="delete"
            onClick={{props.onClick}}
        >
            <AddCircleIcon />
        </IconButton>
    );
}}

export default AddLinkButton;
</document_content>
</document>
<document index="6">
<source>
src/ui/AlertMessage.js
</source>
<document_content>
import React from "react";
import Alert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";
import Slide from '@mui/material/Slide';


function AlertMessage(props) {{
    return (
        <div>
            <Snackbar
                open={{props.open}}
                autoHideDuration={{props.timeout}}
                onClose={{props.handleClose}}
                anchorOrigin={{{{ vertical: "top", horizontal: "right" }}}}
                TransitionComponent={{SlideTransition}}
            >
                <Alert
                    onClose={{props.handleClose}}
                    severity={{props.messageType}}
                    variant="outlined"
                    sx={{{{ width: '100%' }}}}
                    >
                    {{ props.message }}
                </Alert>
            </Snackbar>
        </div>
    );
}}

function SlideTransition(props) {{
    return <Slide {{...props}} direction="down" />;
}}

export default AlertMessage;
</document_content>
</document>
<document index="7">
<source>
src/ui/App.js
</source>
<document_content>
import React, {{ useState }} from 'react';
import {{ v4 as uuid }} from "uuid";
import '../css/App.css';

import GitLink from './GitLink';
import Box from '@mui/material/Box';
import GenerateButton from './GenerateButton';
import Footer from './Footer';
import AddLinkButton from './AddLinkButton';
import AlertMessage from './AlertMessage'

import {{ fetchGeneration, checkLink, checkBranch, formatLinkBranch }} from '../util/util';

function App() {{
  const [repos, setRepos] = useState([
    {{
      id: uuid(),
      link: "https://github.com/sachinreddy1/YetiBackend",
      branch: "main",
      linkError: false,
      branchError: false
    }}
  ])

  // --------------------

  const addRepo = () => {{
    const newList = repos.concat(
      {{
        id: uuid(),
        link: "",
        branch: "",
        linkError: false,
        branchError: false,
      }}
    )
    setRepos(newList);
  }}

  const updateRepoLink = (id, newLink) => {{
    setRepos((prevRepos) => {{
      return prevRepos.map((repo) => {{
        if (repo.id === id) {{
          return {{ ...repo, link: newLink }};
        }}
        return repo;
      }});
    }});
  }};

  const updateRepoBranch = (id, newBranch) => {{
    setRepos((prevRepos) => {{
      return prevRepos.map((repo) => {{
        if (repo.id === id) {{
          return {{ ...repo, branch: newBranch }};
        }}
        return repo;
      }});
    }});
  }};

  const deleteRepo = (id) => {{
    const newList = repos.filter((repo) => repo.id !== id);
    setRepos(newList);
  }}

  const [snackbarMessage, setSnackbarMessage] = React.useState(null);

  function handleCloseSnackbar(event, reason) {{
      if (reason === "clickaway") {{
          return;
      }}
      setSnackbarMessage(null);
  }}

  // --------------------

  const generateDiagram = () => {{
    var allReposValid = true

    setRepos((prevRepos) => {{
      return prevRepos.map((repo) => {{
        const linkValid = checkLink(repo);
        const branchValid = checkBranch(repo);

        allReposValid = (allReposValid && linkValid && branchValid)

        return {{
          ...repo,
          linkError: !linkValid,
          branchError: !branchValid,
        }};
      }});
    }});

    if (allReposValid) {{
      const data = formatLinkBranch(repos)
      console.log(data)
      fetchGeneration(data, setSnackbarMessage)
    }}
  }}

  // --------------------

  return (
    <div className="App">
      <header className="App-header">
        <AlertMessage
          open={{snackbarMessage !== null}}
          message={{snackbarMessage !== null ? snackbarMessage.message : ""}}
          messageType={{snackbarMessage !== null ? snackbarMessage.type : ""}}
          timeout={{snackbarMessage !== null ? snackbarMessage.timeout : 0}}
          handleClose={{handleCloseSnackbar}}
        />

        <Box sx={{{{ m: 0, display: 'flex', flexWrap: 'wrap', justifyContent: 'center'}}}}>
          {{repos.map((repo, index) =>
            <GitLink
              index={{index}}

              repo={{repo}}
              link={{repo.link}}
              branch={{repo.branch}}

              linkError={{repo.linkError}}
              branchError={{repo.branchError}}

              onDelete={{deleteRepo}}
              onChangeLink={{updateRepoLink}}
              onChangeBranch={{updateRepoBranch}}
            />
          )}};
        </Box>

        {{
          repos.length <= 5 ?
          <AddLinkButton
            onClick={{addRepo}}
          /> :
          ""
        }}

        <GenerateButton
          onClick={{generateDiagram}}
        />
        <Footer/>
      </header>
    </div>
  );
}}

export default App;

</document_content>
</document>
<document index="8">
<source>
src/ui/Footer.js
</source>
<document_content>
import React from "react";

function Footer() {{
  return (
    <div className="footer">
      <div className="footerText">v0.1</div>
    </div>
  );
}}

export default Footer;

</document_content>
</document>
<document index="9">
<source>
src/ui/GenerateButton.js
</source>
<document_content>
import React from "react";
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';

function GenerateButton(props) {{
    return (
        <div className="generateButton">
            <Button
                variant="contained"
                onClick={{props.onClick}}
                endIcon={{<SendIcon />}}
            >
                Generate
            </Button>
        </div>
    );
}}

export default GenerateButton;
</document_content>
</document>
<document index="10">
<source>
src/ui/GitLink.js
</source>
<document_content>
import React from "react";
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';

function GitLink(props) {{
    const defaultLink = "https://github.com/{{owner}}/{{repository}}"
    const defaultBranch = "master"

    return (
        <div className="flex-container">
            <TextField
                required
                error={{props.linkError}}

                helperText={{props.linkError ? "GitHub link format is incorrect." : ""}}
                sx={{{{ m: 1.5, width: '40vw' }}}}
                label="Git Link"
                placeholder={{defaultLink}}
                value={{props.link}}
                onChange={{(e) => props.onChangeLink(props.repo.id, e.target.value)}}
            />

            <TextField
                required
                error={{props.branchError}}

                helperText={{props.branchError ? "Branch must be non-empty." : ""}}
                sx={{{{ m: 1.5, width: '10vw' }}}}
                label="Branch"
                placeholder={{defaultBranch}}
                value={{props.branch}}
                onChange={{(e) => props.onChangeBranch(props.repo.id, e.target.value)}}
            />

            <div className="parentElement">
                {{
                    props.index !== 0 ?
                        <div className="centered-element">
                            <IconButton
                                aria-label="delete"
                                size="medium"
                                onClick={{() => props.onDelete(props.repo.id)}}
                                sx={{{{ padding: 0, margin: 4 }}}}
                            >
                                <DeleteIcon fontSize="inherit" />
                            </IconButton>
                        </div>
                    : <br/>
                }}
            </div>

        </div>
    );
}}

export default GitLink;
</document_content>
</document>
<document index="11">
<source>
src/util/util.js
</source>
<document_content>
import axios from 'axios';

export const fetchGeneration = (data, setSnackbarMessage) => {{
    setSnackbarMessage({{
        message: "Generating Diagram. This can take up to a minute.",
        type: "info",
        timeout: 20000
    }})

    const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT;
    axios.post(API_ENDPOINT, data, {{
      headers: {{
        'Content-Type': 'application/json',
      }},
    }})
      .then((response) => {{
        // console.log(response.data)
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'diagram.svg'); // or extract the filename from content-disposition
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
        setSnackbarMessage({{
            message: "Diagram generated! Check your downloads folder.",
            type: "success",
            timeout: 8000
        }})
      }})
      .catch((error) => {{
        setSnackbarMessage({{
            message: "Failed to generate diagram. Please reach out if the problem persists.",
            type: "error",
            timeout: 8000
        }})
      }});
  }};

const regex = /https:\/\/github\.com\/([^\/]+)\/([^\/]+)/;

export const checkLink = (repo) => {{
    if (repo.link.match(regex)) {{
      return true
    }} else {{
      return false
    }}
  }}

export const checkBranch = (repo) => {{
    if (repo.branch.length > 0) {{
      return true
    }} else {{
      return false
    }}
  }}

export const formatLinkBranch = (repos) => {{
    return repos.map((repo) => {{
      const match = repo.link.match(regex);

      const owner = match[1];
      const repository = match[2];
      const branch = repo.branch;

      return {{
        owner: owner,
        repository: repository,
        branch: branch,
      }}
    }});
  }}
</document_content>
</document>
</repository>

Output:

graph LR
    A[App.js\n\n Description: Main component of the React application. Handles state and rendering of other components.] --> B[GitLink.js\n\n Description: Component for rendering a single repository link and branch input field.]
    A --> C[AddLinkButton.js\n\n Description: Button component for adding a new repository link.]
    A --> D[GenerateButton.js\n\n Description: Button component for generating the diagram.]
    A --> E[Footer.js\n\n Description: Component for rendering the footer.]
    A --> F[AlertMessage.js\n\n Description: Component for displaying alert messages.]
    A --> G[util.js\n\n External API call: https://s3.console.aws.amazon.com/codeflow/v1/generate\n Description: Utility functions for fetching diagram generation, validating repository links and branches, and formatting data.]
    
If the class is a controller or has a GET, POST, PUT, DELETE endpoint, include the access path in the format: (HelloWorldController.kt\n\n Access Path - GET: /hello). Make sure to add 2 newline characters after the class name.
If a class is making an external API call, include the url that is being called next to the class name, in the format:  (HelloWorldService.kt\n\n https://helloworld.com/hello). Make sure to add 2 newline characters after the class name.
Add a description of what the class is doing. Do this in the format: (GithubContentApiApplication.kt\n\n Description: Main class of the Springboot application.). If the class has an external API call or an Access Path, do it in the format: (GitHubContentController.kt\n\n Access Path: /v1/github/content\n Description: Entry point for the GitHub Content Service.).

Do not include mock classes used for testing in the final flowchart.
Do not include testing classes in the final flowchart.
Do not include data classes, or classes only used by functions to pass data along (strings, objects) in the final flowchart.
Make sure to remove all special character ({{, }}, ?) from links/paths, for example https://api.github.com/repos/{{owner}}/{{repository}}/git/trees/{{branch}}?recursive=true should be changed to https://api.github.com/repos/owner/repository/git/trees/branch?recursive=true and /api/v1/employees/{{id}} should be changed to /api/v1/employees/id .
"""

SINGLE_GENERATION_HUMAN = """
Given the following source code:

{code}

Create a flowchart using Mermaid syntax. Each major class is a node, and links to all the user created classes it references. 
"""

MULTI_GENERATION_TEMPLATE="""
You take source code and generates a flowchart in Mermaid syntax. Only reply with the Mermaid syntax, starting with 'graph LR'.

An example of the correct input/output would be:
Input:

<repository index="1">
<repository_source>
sachinreddy1/CodeFlowUI/main
</repository_source>
<document index="1">
<source>
src/index.js
</source>
<document_content>
import React from 'react';
import ReactDOM from 'react-dom/client';
import './css/App.css';
import App from './ui/App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

</document_content>
</document>
<document index="2">
<source>
src/reportWebVitals.js
</source>
<document_content>
const reportWebVitals = onPerfEntry => {{
  if (onPerfEntry && onPerfEntry instanceof Function) {{
    import('web-vitals').then(({{ getCLS, getFID, getFCP, getLCP, getTTFB }}) => {{
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    }});
  }}
}};

export default reportWebVitals;

</document_content>
</document>
<document index="3">
<source>
src/test/App.test.js
</source>
<document_content>
import {{ render, screen }} from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {{
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
}});

</document_content>
</document>
<document index="4">
<source>
src/test/setupTests.js
</source>
<document_content>
// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

</document_content>
</document>
<document index="5">
<source>
src/ui/AddLinkButton.js
</source>
<document_content>
import React from "react";
import IconButton from '@mui/material/IconButton';
import AddCircleIcon from '@mui/icons-material/AddCircle';

function AddLinkButton(props) {{
    return (
        <IconButton
            aria-label="delete"
            onClick={{props.onClick}}
        >
            <AddCircleIcon />
        </IconButton>
    );
}}

export default AddLinkButton;
</document_content>
</document>
<document index="6">
<source>
src/ui/AlertMessage.js
</source>
<document_content>
import React from "react";
import Alert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";
import Slide from '@mui/material/Slide';


function AlertMessage(props) {{
    return (
        <div>
            <Snackbar
                open={{props.open}}
                autoHideDuration={{props.timeout}}
                onClose={{props.handleClose}}
                anchorOrigin={{{{ vertical: "top", horizontal: "right" }}}}
                TransitionComponent={{SlideTransition}}
            >
                <Alert
                    onClose={{props.handleClose}}
                    severity={{props.messageType}}
                    variant="outlined"
                    sx={{{{ width: '100%' }}}}
                    >
                    {{ props.message }}
                </Alert>
            </Snackbar>
        </div>
    );
}}

function SlideTransition(props) {{
    return <Slide {{...props}} direction="down" />;
}}

export default AlertMessage;
</document_content>
</document>
<document index="7">
<source>
src/ui/App.js
</source>
<document_content>
import React, {{ useState }} from 'react';
import {{ v4 as uuid }} from "uuid";
import '../css/App.css';

import GitLink from './GitLink';
import Box from '@mui/material/Box';
import GenerateButton from './GenerateButton';
import Footer from './Footer';
import AddLinkButton from './AddLinkButton';
import AlertMessage from './AlertMessage'

import {{ fetchGeneration, checkLink, checkBranch, formatLinkBranch }} from '../util/util';

function App() {{
  const [repos, setRepos] = useState([
    {{
      id: uuid(),
      link: "https://github.com/sachinreddy1/YetiBackend",
      branch: "main",
      linkError: false,
      branchError: false
    }}
  ])

  // --------------------

  const addRepo = () => {{
    const newList = repos.concat(
      {{
        id: uuid(),
        link: "",
        branch: "",
        linkError: false,
        branchError: false,
      }}
    )
    setRepos(newList);
  }}

  const updateRepoLink = (id, newLink) => {{
    setRepos((prevRepos) => {{
      return prevRepos.map((repo) => {{
        if (repo.id === id) {{
          return {{ ...repo, link: newLink }};
        }}
        return repo;
      }});
    }});
  }};

  const updateRepoBranch = (id, newBranch) => {{
    setRepos((prevRepos) => {{
      return prevRepos.map((repo) => {{
        if (repo.id === id) {{
          return {{ ...repo, branch: newBranch }};
        }}
        return repo;
      }});
    }});
  }};

  const deleteRepo = (id) => {{
    const newList = repos.filter((repo) => repo.id !== id);
    setRepos(newList);
  }}

  const [snackbarMessage, setSnackbarMessage] = React.useState(null);

  function handleCloseSnackbar(event, reason) {{
      if (reason === "clickaway") {{
          return;
      }}
      setSnackbarMessage(null);
  }}

  // --------------------

  const generateDiagram = () => {{
    var allReposValid = true

    setRepos((prevRepos) => {{
      return prevRepos.map((repo) => {{
        const linkValid = checkLink(repo);
        const branchValid = checkBranch(repo);

        allReposValid = (allReposValid && linkValid && branchValid)

        return {{
          ...repo,
          linkError: !linkValid,
          branchError: !branchValid,
        }};
      }});
    }});

    if (allReposValid) {{
      const data = formatLinkBranch(repos)
      console.log(data)
      fetchGeneration(data, setSnackbarMessage)
    }}
  }}

  // --------------------

  return (
    <div className="App">
      <header className="App-header">
        <AlertMessage
          open={{snackbarMessage !== null}}
          message={{snackbarMessage !== null ? snackbarMessage.message : ""}}
          messageType={{snackbarMessage !== null ? snackbarMessage.type : ""}}
          timeout={{snackbarMessage !== null ? snackbarMessage.timeout : 0}}
          handleClose={{handleCloseSnackbar}}
        />

        <Box sx={{{{ m: 0, display: 'flex', flexWrap: 'wrap', justifyContent: 'center'}}}}>
          {{repos.map((repo, index) =>
            <GitLink
              index={{index}}

              repo={{repo}}
              link={{repo.link}}
              branch={{repo.branch}}

              linkError={{repo.linkError}}
              branchError={{repo.branchError}}

              onDelete={{deleteRepo}}
              onChangeLink={{updateRepoLink}}
              onChangeBranch={{updateRepoBranch}}
            />
          )}};
        </Box>

        {{
          repos.length <= 5 ?
          <AddLinkButton
            onClick={{addRepo}}
          /> :
          ""
        }}

        <GenerateButton
          onClick={{generateDiagram}}
        />
        <Footer/>
      </header>
    </div>
  );
}}

export default App;

</document_content>
</document>
<document index="8">
<source>
src/ui/Footer.js
</source>
<document_content>
import React from "react";

function Footer() {{
  return (
    <div className="footer">
      <div className="footerText">v0.1</div>
    </div>
  );
}}

export default Footer;

</document_content>
</document>
<document index="9">
<source>
src/ui/GenerateButton.js
</source>
<document_content>
import React from "react";
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';

function GenerateButton(props) {{
    return (
        <div className="generateButton">
            <Button
                variant="contained"
                onClick={{props.onClick}}
                endIcon={{<SendIcon />}}
            >
                Generate
            </Button>
        </div>
    );
}}

export default GenerateButton;
</document_content>
</document>
<document index="10">
<source>
src/ui/GitLink.js
</source>
<document_content>
import React from "react";
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';

function GitLink(props) {{
    const defaultLink = "https://github.com/{{owner}}/{{repository}}"
    const defaultBranch = "master"

    return (
        <div className="flex-container">
            <TextField
                required
                error={{props.linkError}}

                helperText={{props.linkError ? "GitHub link format is incorrect." : ""}}
                sx={{{{ m: 1.5, width: '40vw' }}}}
                label="Git Link"
                placeholder={{defaultLink}}
                value={{props.link}}
                onChange={{(e) => props.onChangeLink(props.repo.id, e.target.value)}}
            />

            <TextField
                required
                error={{props.branchError}}

                helperText={{props.branchError ? "Branch must be non-empty." : ""}}
                sx={{{{ m: 1.5, width: '10vw' }}}}
                label="Branch"
                placeholder={{defaultBranch}}
                value={{props.branch}}
                onChange={{(e) => props.onChangeBranch(props.repo.id, e.target.value)}}
            />

            <div className="parentElement">
                {{
                    props.index !== 0 ?
                        <div className="centered-element">
                            <IconButton
                                aria-label="delete"
                                size="medium"
                                onClick={{() => props.onDelete(props.repo.id)}}
                                sx={{{{ padding: 0, margin: 4 }}}}
                            >
                                <DeleteIcon fontSize="inherit" />
                            </IconButton>
                        </div>
                    : <br/>
                }}
            </div>

        </div>
    );
}}

export default GitLink;
</document_content>
</document>
<document index="11">
<source>
src/util/util.js
</source>
<document_content>
import axios from 'axios';

export const fetchGeneration = (data, setSnackbarMessage) => {{
    setSnackbarMessage({{
        message: "Generating Diagram. This can take up to a minute.",
        type: "info",
        timeout: 20000
    }})

    const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT;
    axios.post(API_ENDPOINT, data, {{
      headers: {{
        'Content-Type': 'application/json',
      }},
    }})
      .then((response) => {{
        // console.log(response.data)
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'diagram.svg'); // or extract the filename from content-disposition
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
        setSnackbarMessage({{
            message: "Diagram generated! Check your downloads folder.",
            type: "success",
            timeout: 8000
        }})
      }})
      .catch((error) => {{
        setSnackbarMessage({{
            message: "Failed to generate diagram. Please reach out if the problem persists.",
            type: "error",
            timeout: 8000
        }})
      }});
  }};

const regex = /https:\/\/github\.com\/([^\/]+)\/([^\/]+)/;

export const checkLink = (repo) => {{
    if (repo.link.match(regex)) {{
      return true
    }} else {{
      return false
    }}
  }}

export const checkBranch = (repo) => {{
    if (repo.branch.length > 0) {{
      return true
    }} else {{
      return false
    }}
  }}

export const formatLinkBranch = (repos) => {{
    return repos.map((repo) => {{
      const match = repo.link.match(regex);

      const owner = match[1];
      const repository = match[2];
      const branch = repo.branch;

      return {{
        owner: owner,
        repository: repository,
        branch: branch,
      }}
    }});
  }}
</document_content>
</document>
</repository>
<repository index="2">
<repository_source>
sachinreddy1/CodeFlowBackend/main
</repository_source>
<document index="1">
<source>
app.py
</source>
<document_content>
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import RepositoryInfo
from typing import List
from generate import Generator
from dotenv import load_dotenv

load_dotenv()
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key

app = Flask(__name__)
CORS(app)

@app.route('/v1/generate', methods=['POST'])
def generate():
    if not request.json:
        return jsonify({{'error': 'Request body must be JSON'}}), 400

    data = request.json

    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        return jsonify({{'error': 'Invalid JSON format'}}), 400

    repos: List[RepositoryInfo] = [RepositoryInfo(**item) for item in data]
    return Generator.generateDiagram(repos)

if __name__ == "__main__":
    app.run(debug=True)
</document_content>
</document>
<document index="3">
<source>
generate.py
</source>
<document_content>
from flask import jsonify
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from constants import SINGLE_GENERATION_TEMPLATE, HUMAN
from githubContent import GithubContent
from krokiClient import KrokiClient

class Generator:
    def generateDiagram(repos):
        num_repos = len(repos)
        if (num_repos == 0):
            return jsonify({{'error': 'No repositories provided.'}}), 400
        elif (num_repos == 1):
            return Generator.single_generation(repos)
        else:
            return Generator.multi_generation(repos)

    def single_generation(repos):
        tree = GithubContent.getGitHubTree(repos[0])
        code = GithubContent.getContentString(repos[0], tree, 1)

        chat = ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229")
        system = (SINGLE_GENERATION_TEMPLATE)
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", HUMAN)])
        chain = prompt | chat
        response = chain.invoke({{"code": code}})
        return KrokiClient.getMermaidSVG(response.content)

    def multi_generation(repos):
        index = 1
        code = ""
        for repo in repos:
            tree = GithubContent.getGitHubTree(repo)
            code += GithubContent.getContentString(repo, tree, index)
            index += 1

        return jsonify({{'message': 'JSON processed successfully'}}), 200


</document_content>
</document>
<document index="4">
<source>
githubContent.py
</source>
<document_content>
from flask import jsonify
from util import Util
from models import GitHubTreeResponse, GitHubBlobResponse
import requests
from dotenv import load_dotenv
import os

load_dotenv()
github_auth_token = os.getenv('GITHUB_AUTH_TOKEN')
github_tree_url = os.getenv('GITHUB_TREE_URL')
headers = {{
    'Authorization': github_auth_token,
}}

class GithubContent:
    def getGitHubTree(repo):
        formatted_url = github_tree_url.format(repo.owner, repo.repository, repo.branch)
        response = requests.get(formatted_url, headers=headers)
        if response.status_code == 200:
            github_tree_response = GitHubTreeResponse.from_json(response.text)
            tree = github_tree_response.tree
            return tree
        else:
            return jsonify({{'error': 'Unable to fetch repository.'}}), 400

    def getGitHubBlob(url):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            github_blob_response = GitHubBlobResponse.from_json(response.text)
            content = github_blob_response.content
            return content
        else:
            return jsonify({{'error': 'Unable to fetch repository information.'}}), 400

    def getContentString(repo, tree, i):
        ret = f"<repository index=\"{{i}}\">\n"

        ret += f"<repository_source>\n"
        ret += f"{{"{{}}/{{}}/{{}}".format(repo.owner, repo.repository, repo.branch)}}\n"
        ret += f"</repository_source>\n"

        index = 1
        for i in tree:
            if (Util.isValidFileType(i.path)):
                blob = GithubContent.getGitHubBlob(i.url)
                if (blob):
                    ret += f"<document index=\"{{index}}\">\n"
                    ret += f"<source>\n"
                    ret += f"{{i.path}}\n"
                    ret += f"</source>\n"
                    ret += f"<document_content>\n"
                    ret += f"{{Util.decodeBase64(blob)}}\n"
                    ret += f"</document_content>\n"
                    ret += f"</document>\n"

                    index += 1

        ret += "</repository>\n"
        return ret
</document_content>
</document>
<document index="5">
<source>
krokiClient.py
</source>
<document_content>
from flask import jsonify, Response
import requests

class KrokiClient:
    def getMermaidSVG(data):
        url = "https://kroki.io/mermaid/svg"
        headers = {{
            'Content-Type': 'text/plain',
        }}

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return Response(response.content, mimetype='image/svg+xml', headers={{"Content-disposition": 'attachment; filename="diagram.svg"'}})
        else:
            return jsonify({{'error': 'Unable to fetch SVG.'}}), 400
</document_content>
</document>
<document index="6">
<source>
models.py
</source>
<document_content>
from dataclasses import dataclass
from typing import List, Optional
from dataclasses_json import dataclass_json

@dataclass
class RepositoryInfo:
    owner: str
    repository: str
    branch: str

@dataclass_json
@dataclass
class GitHubTreeFile:
    path: str
    url: str

@dataclass_json
@dataclass
class GitHubTreeResponse:
    tree: List[GitHubTreeFile]

@dataclass_json
@dataclass
class GitHubBlobResponse:
    content: Optional[str] = None

</document_content>
</document>
<document index="7">
<source>
util.py
</source>
<document_content>
import base64

class Util:
    def decodeBase64(encodedString):
        decoded_bytes = base64.b64decode(encodedString)
        decoded_string = decoded_bytes.decode('iso-8859-1')
        return decoded_string

    def isValidFileType(path):
        validFileTypes = ["py", "js", "kt", "java", "yml", ".production"]

        if ('.' in path):
            s = path.split('.')
            if s[-1] in validFileTypes:
                return True
        return False
</document_content>
</document>
</repository>
<repository index="3">
<repository_source>
sachinreddy1/YetiBackend/main
</repository_source>
<document index="1">
<source>
src/main/kotlin/com/sachinreddy/yetibackend/YetibackendApplication.kt
</source>
<document_content>
package com.sachinreddy.yetibackend

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class YetibackendApplication

fun main(args: Array<String>) {{
        runApplication<YetibackendApplication>(*args)
}}

</document_content>
</document>
<document index="2">
<source>
src/main/kotlin/com/sachinreddy/yetibackend/controller/HelloWorldController.kt
</source>
<document_content>
package com.sachinreddy.yetibackend.controller

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("hello")
class HelloWorldController {{
    @GetMapping
    fun helloWorld(): String = "Hello world!! :D"
}}
</document_content>
</document>
<document index="3">
<source>
src/main/kotlin/com/sachinreddy/yetibackend/controller/YetiPostController.kt
</source>
<document_content>
package com.sachinreddy.yetibackend.controller

import com.sachinreddy.yetibackend.model.YetiPost
import com.sachinreddy.yetibackend.service.YetiPostService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("v1/posts")
class YetiPostController @Autowired constructor(
    private val yetiPostService: YetiPostService
) {{
    @GetMapping
    fun getPosts(): List<YetiPost> {{
        return yetiPostService.getPosts()
    }}

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun addPost(@RequestBody post: YetiPost): List<YetiPost> {{
        return yetiPostService.addPost(post)
    }}
}}
</document_content>
</document>
<document index="4">
<source>
src/main/kotlin/com/sachinreddy/yetibackend/dao/MockYetiPostDao.kt
</source>
<document_content>
package com.sachinreddy.yetibackend.dao

import com.sachinreddy.yetibackend.model.YetiPost
import org.springframework.stereotype.Repository
import java.util.*

@Repository
class MockYetiPostDao: YetiPostDao {{
    private val posts = mutableListOf(
        YetiPost(UUID.randomUUID(), "sachinreddy", 3, ""),
        YetiPost(UUID.randomUUID(), "bilbobagins", 6, ""),
        YetiPost(UUID.randomUUID(), "frodobagins", 2, ""),
        YetiPost(UUID.randomUUID(), "dunkey", 12, "")
    )

    override fun getPosts(): List<YetiPost> {{
        return posts
    }}

    override fun insertPost(id: UUID, post: YetiPost): List<YetiPost> {{
        posts.add(YetiPost(id, post.userName, post.numLikes, post.imageURI))
        return posts
    }}
}}
</document_content>
</document>
<document index="5">
<source>
src/main/kotlin/com/sachinreddy/yetibackend/dao/YetiPostDao.kt
</source>
<document_content>
package com.sachinreddy.yetibackend.dao

import com.sachinreddy.yetibackend.model.YetiPost
import java.util.UUID

interface YetiPostDao {{
    fun getPosts(): List<YetiPost>

    fun insertPost(id: UUID, post: YetiPost): List<YetiPost>

    fun addPerson(post: YetiPost): List<YetiPost> {{
        val id = UUID.randomUUID()
        return insertPost(id, post)
    }}
}}
</document_content>
</document>
<document index="6">
<source>
src/main/kotlin/com/sachinreddy/yetibackend/model/YetiPost.kt
</source>
<document_content>
package com.sachinreddy.yetibackend.model

import com.fasterxml.jackson.annotation.JsonProperty
import java.util.UUID

data class YetiPost(
    @JsonProperty("id")
    val id: UUID?,

    @JsonProperty("userName")
    val userName: String,

    @JsonProperty("numLikes")
    val numLikes: Int,

    @JsonProperty("imageURI")
    val imageURI: String
)
</document_content>
</document>
<document index="7">
<source>
src/main/kotlin/com/sachinreddy/yetibackend/service/YetiPostService.kt
</source>
<document_content>
package com.sachinreddy.yetibackend.service

import com.sachinreddy.yetibackend.dao.YetiPostDao
import com.sachinreddy.yetibackend.model.YetiPost
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.stereotype.Service

@Service
class YetiPostService @Autowired constructor(
    private val yetiPostDao: YetiPostDao
) {{
    fun getPosts(): List<YetiPost> {{
        return yetiPostDao.getPosts()
    }}

    fun addPost(post: YetiPost): List<YetiPost> {{
        return yetiPostDao.addPerson(post)
    }}
}}
</document_content>
</document>
<document index="8">
<source>
src/test/kotlin/com/sachinreddy/yetibackend/YetibackendApplicationTests.kt
</source>
<document_content>
package com.sachinreddy.yetibackend

import org.junit.jupiter.api.Test
import org.springframework.boot.test.context.SpringBootTest

@SpringBootTest
class YetibackendApplicationTests {{

        @Test
        fun contextLoads() {{
        }}

}}

</document_content>
</document>
<document index="9">
<source>
src/test/kotlin/com/sachinreddy/yetibackend/controller/YetiPostControllerTest.kt
</source>
<document_content>
package com.sachinreddy.yetibackend.controller

import com.fasterxml.jackson.databind.ObjectMapper
import com.sachinreddy.yetibackend.model.YetiPost
import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.http.MediaType
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.get
import org.springframework.test.web.servlet.post
import java.util.*

@SpringBootTest
@AutoConfigureMockMvc
internal class YetiPostControllerTest @Autowired constructor(
    val mockMvc: MockMvc,
    val objectMapper: ObjectMapper
){{
    val baseUrl = "/v1/posts"

    @Test
    fun `should return all posts`() {{
        // when
        val posts = mockMvc.get(baseUrl)
            .andDo {{ print() }}
            .andExpect {{
                status {{ isOk()}}
                content {{ contentType(MediaType.APPLICATION_JSON) }}

            }}
    }}

    @Test
    fun `should add a post`() {{
        // given
        val newPost = YetiPost(UUID.randomUUID(), "test", 3, "")

        // when
        val performPost = mockMvc.post(baseUrl) {{
            contentType = MediaType.APPLICATION_JSON
            content = objectMapper.writeValueAsString(newPost)
        }}

        // then
        performPost
            .andDo {{ print() }}
                .andExpect {{
                    status {{ isCreated() }}
                    content {{ contentType(MediaType.APPLICATION_JSON) }}
                }}
    }}
}}
</document_content>
</document>
<document index="10">
<source>
src/test/kotlin/com/sachinreddy/yetibackend/dao/MockYetiPostDaoTest.kt
</source>
<document_content>
package com.sachinreddy.yetibackend.dao

import org.assertj.core.api.Assertions.*
import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.Test

internal class MockYetiPostDaoTest {{
    private val mockYetiPostDao = MockYetiPostDao()

    @Test
    fun `should provide a list of yeti posts`() {{
        //given

        //when
        val posts = mockYetiPostDao.getPosts()

        // then
        assertThat(posts).isNotEmpty
    }}

    @Test
    fun `should provide some mock data`() {{
        //given

        //when
        val posts = mockYetiPostDao.getPosts()

        // then
        assertThat(posts).allMatch {{
            it.userName.isNotBlank()
        }}
    }}
}}
</document_content>
</document>
<document index="11">
<source>
src/test/kotlin/com/sachinreddy/yetibackend/service/YetiPostServiceTest.kt
</source>
<document_content>
package com.sachinreddy.yetibackend.service

import com.sachinreddy.yetibackend.dao.YetiPostDao
import io.mockk.mockk
import io.mockk.verify
import org.junit.jupiter.api.Test

internal class YetiPostServiceTest {{
    private val dataSource: YetiPostDao = mockk(relaxed = true)
    private val postService = YetiPostService(dataSource)

    @Test
    fun `should call data source to receive banks`() {{
        // given

        // when
        postService.getPosts()

        // then
        verify(exactly = 1) {{ dataSource.getPosts() }}
    }}
}}
</document_content>
</document>
</repository>

Output:

graph LR
    A[CodeFlowUI\n\n Description: Frontend, React web application to generate flowcharts given one or multiple GitHub repositories.] -->|POST: v1/generate| B[CodeFlowBackend\n\n Access Path - POST: /v1/generate\n Description: Backend, Flask application to generate flowcharts given one or multiple GitHub repositories.\n Calls GitHub API to obtain all the code in the repositories. Then calls Kroki's API to generate an SVG based on the generated Mermaid syntax.]
    B -->|GET: https://api.github.com/repos/owner/repository/branch| D[External API call: GitHub API\n\n Description: Obtains the file structure and contents of a GitHub repository.]
    B -->|POST: api.anthropic.com| E[External API call: Anthropic API\n\n Description: Given source code, will generate Mermaid syntax to create a flowchart.]
    B -->|POST: https://kroki.io/mermaid/svg| F[External API call: Kroki API\n\n Description: Given Mermaid syntax, will generate an SVG.]
    C[YetiBackend\n\n Access Path - GET: /v1/posts\n Description: Backend, Springboot application with a mock database. Has endpoints to get and create posts.]

Each node in the flowchart is either a repository or an external API call. For example, the repository: CodeFlowUI should have a node in the format (A[CodeFlowUI\n\n Description: Frontend, React web application to generate flowcharts given one or multiple GitHub repositories.]).
If a repository/node is calling another repository/node or an external, make sure to label the connection with the endpoint being called. For example:  A[ExampleUI\n\n Description: Example description.] -->|GET: v1/example| B[ExampleBackend\n\n Access Path - GET: /v1/example\n Description: Example description.]
If an external API call is made, it should be in the format: (E[External API call: Kroki API\n\n Description: Given Mermaid syntax, will generate an SVG.]). The title of the API called on top along with the description for the API call and what it does.
If a description is too long, then add a \n character to make the description more readable like: (Description: Backend, Flask application to generate flowcharts given one or multiple GitHub repositories.\n Calls GitHub API to obtain all the code in the repositories. Then calls Kroki's API to generate an SVG based on the generated Mermaid syntax.]).
Make sure to remove all special character ({{, }}, ?) from links/paths, for example https://api.github.com/repos/{{owner}}/{{repository}}/git/trees/{{branch}}?recursive=true should be changed to https://api.github.com/repos/owner/repository/git/trees/branch?recursive=true and /api/v1/employees/{{id}} should be changed to /api/v1/employees/id .
If there is no API call made between two repositories, do not draw a link between them. In the example provided, CodeFlowUI does not call YetiBackend, so there is no connection there.
"""

MULTI_GENERATION_HUMAN="""
Given the following source code:

{code}

Create a flowchart using Mermaid syntax. Each repository is a node, and links to other repositories it calls or external APIs. 
"""