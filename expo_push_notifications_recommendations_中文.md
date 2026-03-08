# Expo+React Native 消息推送和离线消息解决方案

## 概述
对于 Expo+React Native 应用，实现消息推送和离线消息需要结合以下组件：
1. **推送通知服务** - 用于应用在后台/关闭时接收实时通知
2. **离线消息队列** - 用于设备离线时存储消息
3. **本地通知** - 用于应用在前台时显示通知

## 推荐解决方案

### 1. 推送通知服务

#### 选项 A: Expo 通知系统（Expo 项目推荐）
- **包**: `expo-notifications`
- **优点**:
  - 内置的 Expo 解决方案，集成无缝
  - 跨平台（iOS、Android、Web）
  - 通过 Expo Push Token 系统易于设置
  - 基本使用免费（Expo 推送通知服务）
  - 自动处理 iOS 证书管理
- **缺点**:
  - 仅限于 Expo 基础设施
  - 免费版有速率限制
  - 相比直接使用 FCM/APNs 控制较少

#### 选项 B: Firebase Cloud Messaging (FCM) + React Native Firebase
- **包**: `@react-native-firebase/messaging`
- **优点**:
  - 行业标准，高度可靠
  - 高级定向和数据分析功能
  - 免费额度充足
  - 直接集成 Firebase 生态系统
- **缺点**:
  - 需要从 Expo 弹出或使用 Expo Dev Client
  - 设置更复杂
  - 需要手动处理 iOS 证书

#### 选项 C: OneSignal
- **包**: `react-native-onesignal`
- **优点**:
  - 易于设置，文档完善
  - 提供免费版本
  - 高级用户细分和 A/B 测试
  - 提供 Web 管理面板
- **缺点**:
  - 第三方依赖
  - 可能需要从 Expo 弹出
  - 数据隐私考虑

### 2. 离线消息解决方案

#### 选项 A: AsyncStorage + 自定义队列系统
- **包**: `@react-native-async-storage/async-storage` + 自定义队列
- **方法**:
  - 离线时将接收到的消息存储在 AsyncStorage 中
  - 实现带重试逻辑的消息队列
  - 连接恢复时与服务器同步
- **优点**:
  - 完全控制实现
  - 轻量级，无额外依赖
  - 适用于任何后端
- **缺点**:
  - 需要手动构建队列逻辑
  - 无内置冲突解决机制

#### 选项 B: WatermelonDB
- **包**: `@nozbe/watermelondb`
- **优点**:
  - 内置离线优先架构
  - 可观察查询，支持实时 UI 更新
  - 冲突解决策略
  - 基于 SQLite，性能优秀
- **缺点**:
  - 学习曲线较陡
  - 设置更复杂
  - 对于简单消息功能可能过于复杂

#### 选项 C: Realm 数据库
- **包**: `realm`
- **优点**:
  - 优秀的离线优先支持
  - 实时同步能力（配合 Realm Sync）
  - 性能良好
  - MongoDB 集成
- **缺点**:
  - 需要原生链接（可能需要 Expo Dev Client）
  - 高级功能需要商业许可

### 3. 本地通知（前台）

#### Expo 通知系统 (expo-notifications)
- 同时处理推送通知和本地通知
- 可以调度本地通知
- 适合提醒用户离线消息

## 最优解决方案推荐

### **混合方案：Expo 通知系统 + AsyncStorage + 自定义队列**

#### 架构：
```
┌─────────────────────────────────────────────────────────────┐
│                    推送通知流程                              │
├─────────────────────────────────────────────────────────────┤
│  1. Expo Push Tokens → 后端（存储每个用户的令牌）           │
│  2. 后端通过 Expo Push Service 发送通知                     │
│  3. expo-notifications 接收推送（后台/退出状态）            │
│  4. 如果应用在前台：显示本地通知                            │
│  5. 离线时将消息存储在 AsyncStorage 中                      │
│  6. 在线时与服务器同步                                      │
└─────────────────────────────────────────────────────────────┘
```

#### 实施步骤：

1. **设置 Expo 通知系统**
   ```bash
   npx expo install expo-notifications
   npx expo install expo-device
   ```

2. **配置 iOS/Android 权限**
   - 在 `app.json` 中添加权限配置
   - 配置 iOS 授权
   - 设置 Android 通知渠道

3. **后端实现**
   - 存储每个用户的 Expo push tokens
   - 使用 Expo API 发送通知
   - 为离线用户实现消息持久化

4. **前端实现**
   ```javascript
   // 请求权限并获取 token
   import * as Notifications from 'expo-notifications';
   
   async function registerForPushNotifications() {
     const { status } = await Notifications.requestPermissionsAsync();
     if (status !== 'granted') return;
     
     const token = (await Notifications.getExpoPushTokenAsync()).data;
     // 将 token 发送到您的后端
   }
   
   // 处理接收到的通知
   Notifications.setNotificationHandler({
     handleNotification: async () => ({
       shouldShowAlert: true,
       shouldPlaySound: true,
       shouldSetBadge: true,
     }),
   });
   ```

5. **离线消息队列**
   ```javascript
   // 简单的队列实现
   class MessageQueue {
     constructor() {
       this.queue = [];
       this.isOnline = true;
     }
     
     async addMessage(message) {
       await AsyncStorage.setItem(
         `message_${Date.now()}`,
         JSON.stringify(message)
       );
       if (this.isOnline) {
         await this.syncMessages();
       }
     }
     
     async syncMessages() {
       const keys = await AsyncStorage.getAllKeys();
       const messageKeys = keys.filter(k => k.startsWith('message_'));
       
       for (const key of messageKeys) {
         const message = await AsyncStorage.getItem(key);
         // 发送到服务器
         const success = await sendToServer(JSON.parse(message));
         if (success) {
           await AsyncStorage.removeItem(key);
         }
       }
     }
   }
   ```

6. **网络状态监控**
   ```javascript
   import NetInfo from '@react-native-community/netinfo';
   
   NetInfo.addEventListener(state => {
     if (state.isConnected && queue.hasPendingMessages()) {
       queue.syncMessages();
     }
   });
   ```

## 替代方案：完整的 Firebase 解决方案

如果您需要更高级的功能并且愿意从 Expo 弹出：

1. **React Native Firebase Messaging** 用于推送通知
2. **Firebase Firestore** 带离线持久化
3. **Firebase Cloud Functions** 用于后端逻辑

## 成本考虑

| 解决方案 | 成本 | 最适合 |
|----------|------|----------|
| **Expo 通知系统** | 免费（有限制），有付费计划 | 简单应用，快速 MVP |
| **Firebase** | 免费额度充足，按使用付费 | 需要扩展的生产级应用 |
| **OneSignal** | 免费版本，高级功能付费 | 营销导向的应用 |
| **自定义后端** | 仅服务器成本 | 需要完全控制，特定需求 |

## 实施检查清单

- [ ] 设置 `expo-notifications`
- [ ] 配置 iOS/Android 权限
- [ ] 实现推送 token 注册
- [ ] 构建发送通知的后端端点
- [ ] 使用 AsyncStorage 创建离线消息存储
- [ ] 实现带重试逻辑的消息队列
- [ ] 添加网络状态监控
- [ ] 在 iOS 和 Android 上测试
- [ ] 处理通知点击操作
- [ ] 实现徽章计数管理
- [ ] 添加深度链接支持

## 结论

对于大多数 Expo+React Native 项目，**Expo 通知系统 + AsyncStorage** 组合提供了最佳平衡：
- **易于实施**（保持在 Expo 生态系统内）
- **成本效益**（提供免费版本）
- **可靠性**（Expo 基础设施已可用于生产环境）
- **离线能力**（自定义队列确保消息不丢失）

此解决方案允许您在不从 Expo 弹出或添加复杂依赖的情况下，实现强大的推送通知和离线消息持久化功能。