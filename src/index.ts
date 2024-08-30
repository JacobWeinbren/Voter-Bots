import { BskyAgent, RichText } from "@atproto/api";
import * as dotenv from "dotenv";
import * as path from "path";
import * as fs from "fs/promises";

dotenv.config();

const BLUESKY_HANDLE = process.env.BLUESKY_HANDLE;
const BLUESKY_PASSWORD = process.env.BLUESKY_PASSWORD;

if (!BLUESKY_HANDLE || !BLUESKY_PASSWORD) {
	console.error("Missing Bluesky credentials");
	process.exit(1);
}

async function getNextTweet(): Promise<string> {
	const tweetsPath = path.join(__dirname, "..", "Israel", "tweets.txt");
	const positionPath = path.join(
		__dirname,
		"..",
		"Israel",
		"current_position.txt"
	);

	const content = await fs.readFile(tweetsPath, "utf-8");
	const tweets = content
		.split("\n\n\n")
		.filter((tweet) => tweet.trim() !== "");

	let currentPosition = 0;
	try {
		currentPosition = parseInt(await fs.readFile(positionPath, "utf-8"));
	} catch (error) {
		// If file doesn't exist or is invalid, start from 0
	}

	const tweet = tweets[currentPosition];

	// Update position for next time
	currentPosition = (currentPosition + 1) % tweets.length;
	await fs.writeFile(positionPath, currentPosition.toString());

	return tweet;
}

async function main() {
	const agent = new BskyAgent({ service: "https://bsky.social" });
	await agent.login({
		identifier: BLUESKY_HANDLE!,
		password: BLUESKY_PASSWORD!,
	});

	const tweet = await getNextTweet();
	const rt = new RichText({ text: tweet });
	await rt.detectFacets(agent);

	await agent.post({
		text: rt.text,
		facets: rt.facets,
	});

	console.log("Posted tweet:", tweet);
}

main().catch((error) => {
	console.error("Error:", error);
	process.exit(1);
});
