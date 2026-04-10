# Roadmap

_Last updated: 2026-04-10_

## Progress summary

| Phase | Completion |
|---|---:|
| 1. Foundation and bootstrap | 94% |
| 2. Scanner migration and orchestration | 93% |
| 3. Filtering, evidence, confidence | 92% |
| 4. Output redesign and diffing | 90% |
| 5. Workflow automation and publication | 92% |
| 6. New source expansion | 62% |
| 7. Testing and cutover readiness | 98% |

**Overall estimated completion:** 93%

## Current pass highlights
- Completed a cleanup/tuning pass across scoring, tests, and README accuracy.
- Added Bitbucket confidence-floor coverage so all current active sources are represented in scoring.
- Refreshed README to reflect the real source set and the GitHub Actions execution path.
- Continued tightening late-stage docs and validation parity.

## Approved source expansion shortlist

These are approved for roadmap planning only and are not yet implementation-complete:

### Global / broader Android indexes and stores
- Google Play Store
- Accrescent
- AppBrain
- GetJar
- Aurora Store
- RepoStore
- Obtainium-style source discovery
- APKPure
- APKTime
- AppsAPK
- 9Apps
- Appvn
- ACMarket
- Fossdroid
- AppSales

### China-focused Android indexes and stores
- Huawei AppGallery / 华为应用市场
- Tencent MyApp / 应用宝
- Xiaomi GetApps / 小米应用商店
- OPPO App Store / OPPO软件商店
- Vivo App Store / vivo应用商店
- 360 Mobile Assistant / 360手机助手
- Baidu Mobile Assistant / 百度手机助手
- Wandoujia / 豌豆荚
- CoolAPK / 酷安
- Lenovo App Store
- Flyme store
- 应用汇
- PP助手
- 安智市场

### Recommended source-expansion priority
1. Google Play Store
2. Huawei AppGallery
3. Tencent MyApp
4. Xiaomi GetApps
5. OPPO App Store
6. Vivo App Store
7. Accrescent
8. AppBrain
9. Aurora Store
10. RepoStore
11. 360 Mobile Assistant
12. Baidu Mobile Assistant
13. Wandoujia
14. CoolAPK
15. APKPure

## Next pass targets
- final cleanup pass across docs, env examples, and minor workflow polish
- last confidence/source tuning pass only if anything still looks inconsistent
