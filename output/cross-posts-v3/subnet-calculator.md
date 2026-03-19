---
title: "I Built a Free Subnet Calculator That Runs Entirely in Your Browser"
published: true
tags: webdev, tools, javascript, opensource
canonical_url: https://zovo.one/free-tools/subnet-calculator/
---

Subnetting by hand is a rite of passage in networking. But once you've proven you can do it, there's no reason to keep doing the binary math manually when you're designing a real network. I built a subnet calculator that handles the tedious parts so you can focus on the design.

## What It Does

Enter an IP address and a subnet mask (CIDR or dotted decimal). The calculator gives you the network address, broadcast address, usable host range, number of usable hosts, wildcard mask, and the binary representation of everything.

There's also a subnet splitter — take a network and divide it into a specific number of subnets, and it shows you all the resulting subnet details. Useful for VLSM planning and carving up address space.

## Why I Built This

I was studying for my CCNA and got tired of tabbing between a calculator app and my notes. The online subnet calculators I found were either ancient-looking Java applets or covered in ads. I wanted something clean, fast, and private.

Since I was dealing with IP addresses from lab environments that sometimes mirrored production networks, I didn't want to type those into a random website. This tool doesn't send anything to a server. All the calculation happens in JavaScript in your browser.

## The Binary View

My favorite feature is the binary breakdown. It shows the IP address and subnet mask in binary, with a clear visual divider between the network and host portions. When you're learning subnetting, seeing the binary representation makes the math click in a way that just memorizing the rules doesn't.

## Part of 285+ Free Tools

This lives alongside 285+ other tools at [zovo.one/free-tools](https://zovo.one/free-tools/). There are other networking tools too — DNS lookup, IP lookup, and more. All free, client-side, no signup, no tracking.

**Try it:** [zovo.one/free-tools/subnet-calculator](https://zovo.one/free-tools/subnet-calculator/)

**All tools:** [zovo.one/free-tools](https://zovo.one/free-tools/)

Michael Lip — 285+ free tools at zovo.one
