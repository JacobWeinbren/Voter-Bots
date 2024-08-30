import { BskyAgent } from "@atproto/api";
import * as fs from 'fs'
import * as path from 'path'
import { RichText } from '@atproto/api'

const client = new BskyAgent({ service: 'https://bsky.social' });

async function getRandomTweet(): Promise<string> {
    const tweetsPath = path.join(__dirname, '..', '/Israel/tweets.txt')
    const content = fs.readFileSync(tweetsPath, 'utf-8')
    const tweets = content
        .split('\n\n\n')
        .filter((tweet) => tweet.trim() !== '')
    return tweets[Math.floor(Math.random() * tweets.length)]
}

async function main() {
    await client.login({
        identifier: process.env.BLUESKY_HANDLE!,
        password: process.env.BLUESKY_PASSWORD!,
    })

    const tweet = await getRandomTweet()
    const rt = new RichText({ text: tweet })
    await rt.detectFacets(client)
    
    await client.post({
        text: rt.text,
        facets: rt.facets,
    })
    
    console.log(`Posted: "${tweet.substring(0, 50)}..."`)
}

main().catch(console.error)