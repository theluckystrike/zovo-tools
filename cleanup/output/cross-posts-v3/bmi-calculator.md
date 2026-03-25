---
title: "I Built a Free BMI Calculator That Runs Entirely in Your Browser"
published: true
tags: webdev, tools, javascript, opensource
canonical_url: https://zovo.one/free-tools/bmi-calculator/
---

BMI calculators are everywhere. But most of them either blast you with health product ads right after showing your result, or they want you to sign up for a "personalized health plan." I just wanted the number. So I built one that gives you the number and respects your privacy.

## What It Does

Enter your height and weight (metric or imperial — it handles both), and the tool calculates your BMI with a visual indicator showing where you fall on the scale. It provides the standard WHO categories: underweight, normal, overweight, and obese ranges.

It also shows the healthy weight range for your height, so you have context instead of just a raw number. And it calculates BMI Prime, which is a ratio showing how far above or below the normal threshold you are.

## No Health Data on Someone's Server

Here's the thing about health data: it's incredibly personal. Your height and weight aren't something you want sitting in a database somewhere, potentially getting correlated with your browsing habits for ad targeting.

This calculator runs entirely in your browser. The math is simple — BMI = weight(kg) / height(m)^2 — and JavaScript handles it just fine without a server. Your measurements stay on your device. No cookies, no analytics, no tracking.

## A Note on BMI Limitations

I built this tool, but I also think it's important to be honest: BMI is a rough screening tool, not a health diagnosis. It doesn't account for muscle mass, bone density, age, sex, or body composition. An athlete with high muscle mass might have an "overweight" BMI while being perfectly healthy.

The tool includes these caveats because I think responsible tools should inform, not just calculate.

## One of 285+ Tools

This BMI calculator is part of my collection at [zovo.one/free-tools](https://zovo.one/free-tools/). There are more health calculators too — BMR, calorie, TDEE, body fat percentage. Plus 285+ other tools across categories. All free, all client-side, no signup.

**Try it:** [zovo.one/free-tools/bmi-calculator](https://zovo.one/free-tools/bmi-calculator/)

**All tools:** [zovo.one/free-tools](https://zovo.one/free-tools/)

Michael Lip — 285+ free tools at zovo.one
