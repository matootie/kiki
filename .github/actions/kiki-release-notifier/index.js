const core = require("@actions/core");
const github = require("@actions/github");
const request = require("request-promise-native");

async function run() {
  try {
    const token = core.getInput("accessToken");
    const url = core.getInput("webhookURL");

    const octokit = github.getOctokit(token);
    const { data: release } = await octokit.repos.getLatestRelease({
      owner: "matootie",
      repo: "kiki"
    });

    const options = {
      method: "POST",
      uri: `${url}`,
      json: true,
      headers: {
        "Content-Type": "application/json",
      },
      body: {
        embeds: [
          {
            title: "New release has been launched",
            description: ":rocket:",
            url: `${release.html_url}`,
            color: 16777215,
            thumbnail: {
              url: "https://cdn.discordapp.com/avatars/424301802763190283/fdca2a40c4187bffacbf0c9999bc17a1.png"
            },
            fields: [
              {
                name: "Version Number",
                value: `${release.tag_name}`
              },
              {
                name: "Release Notes",
                value: `${release.body}`
              }
            ],
            footer: {
              text: "Report any issues to an admin."
            }
          }
        ]
      }
    }

    // [error]400 - {"embeds":["0"]}

    await request(options);
  }
  catch (error) {
    core.setFailed(error.message);
  }
}

run()

/*

*/
