SINGLE_GENERATION_TEMPLATE="""
You take source code and generates a flowchart in Mermaid syntax. Only reply with the Mermaid syntax, starting with 'graph LR'.

An example of the correct input/output would be:
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


If the class is a controller or has a GET, POST, PUT, DELETE endpoint, include the access path in the format: (HelloWorldController.kt\n\n Access Path - GET: /hello). Make sure to add 2 newline characters after the class name.
If a class is making an external API call, include the url that is being called next to the class name, in the format:  (HelloWorldService.kt\n\n https://helloworld.com/hello). Make sure to add 2 newline characters after the class name.
Add a description of what the class is doing. Do this in the format: (GithubContentApiApplication.kt\n\n Description: Main class of the Springboot application.). If the class has an external API call or an Access Path, do it in the format: (GitHubContentController.kt\n\n Access Path: /v1/github/content\n Description: Entry point for the GitHub Content Service.).

Do not include mock classes used for testing in the final flowchart.
Do not include testing classes in the final flowchart.
Do not include data classes, or classes only used by functions to pass data along (strings, objects) in the final flowchart.
"""

HUMAN="""
Given the following source code:

{code}

Create a flowchart using Mermaid syntax. Each major class is a node, and links to all the user created classes it references. 
"""
