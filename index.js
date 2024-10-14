/*
    安装依赖: npm install encryptLong crypto-js express
*/

/* -------------------------模拟浏览器环境------------------------- */
const { JSDOM } = require("jsdom");  
  
const DOM = new JSDOM(`  
    <!DOCTYPE html>
    <body>
    </body>
`);  

global.window = DOM.window  
global.navigator = window.navigator
global.document = window.document

/* -------------------------前端常用加解密------------------------- */


/*
    JSEncrypt 基于RSA的加密库
    作者: yinsel
    关键词: JSEncrypt、setPublicKey、encryptLong、decryptLong
*/

const JSEncrypt = require("encryptlong").default;
const jsencrypt = new JSEncrypt()
console.log(jsencrypt)

/*
    CryptoJS 多功能加密库
    作者: yinsel
    关键词: JSEncrypt、setPublicKey、encryptLong、decryptLong
*/
const CryptoJS = require("crypto-js")
console.log(CryptoJS)

/* 
    Express 简易HTTP服务器
*/

const express = require('express');
const app = express();
const port = 3000;  // 服务器监听端口

// 中间件，用于解析JSON格式的请求体
app.use(express.json());

// 创建一个简单的GET路由
app.get('/get', (req, res) => {
    res.send('Hello, Express!');
});

// 创建一个POST路由，处理JSON数据
app.post('/post', (req, res) => {
    // 返回响应，包含接收到的JSON数据
    const jsonData = req.body
    console.log(jsonData)
    res.json({
        data: "Hello Express!"
    });
});

// 启动服务器
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});