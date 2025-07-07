html = '''
<template src="base">

    <child id="title">MBS 作品回顾</child>

    <child id="headimg">../bgs/MBS_Cover_Lossy.png</child>

    <child id="content">
        <style>
            .game-box:hover{
                height: 250px;
                transition: all 0.2s ease-out;
            }
            .game-box{
                transition: all 0.2s ease-out;
            }
            .game-box p{
                padding: 15px;
                margin: 0;
                box-sizing: border-box;
            }
        </style>
        <script>
            function fillTemplate(templateString, data) {
                return templateString.replace(/\${(.*?)}/g, (match, p1) => {
                    return data[p1] || '';
                });
            }
            const template = '<div class="game-box"><div><img src="${img}" alt=""><span><h2>${title}</h2><h3>${author}</h3></span></div><p>${lore}</p></div >'

            maps = [
                {
                    "title": "夢樂園1930",
                    "author": "16bit Samurai",
                    "img": "./imgs/MCC3-夢樂園1930",
                    "lore": "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Maxime eius voluptatem sapiente autem expedita dignissimos rerum ea tenetur, beatae aliquid id magnam blanditiis eveniet neque fuga eos ipsum quidem quisquam?"
                }
            ]
            console.log(maps);
            

            maps.forEach(element => {
                const filled = fillTemplate(template, {
                    title: element.title,
                    img: element.img,
                    author: element.author,
                    lore: element.lore
                });
                document.getElementsByClassName('article').innerHTML += element;
            });




        </script>
        <h1><a href="../">返回上级</a></h1>
        <h2>MCC3 <a onclick="" target="_blank" href="">硬币</a></h2>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC3-夢樂園1930.webp" alt=""><span>
                    <h2>夢樂園1930</h2>
                    <h3>16bit Samurai</h3>
                </span>
            </div>
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt reprehenderit reiciendis at ducimus perferendis adipisci hic ea facilis voluptas sapiente officiis numquam, repudiandae animi soluta temporibus rem alias doloremque autem!</p>
        </div>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC3-命运硬币.webp" alt=""><span>
                    <h2>命运硬币</h2>
                    <h3>DYM</h3>
                </span>
            </div>
        </div>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC3-超电磁炮大乱斗.webp" alt=""><span>
                    <h2>超电磁炮大乱斗</h2>
                    <h3>甘蔗铜西瓜</h3>
                </span>
            </div>
        </div>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC3-疯狂的硬币.webp" alt=""><span>
                    <h2>疯狂的硬币</h2>
                    <h3>鸽子窝</h3>
                </span>
            </div>
        </div>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC3-机会硬币.webp" alt=""><span>
                    <h2>机会硬币</h2>
                    <h3>无限水</h3>
                </span>
            </div>
        </div>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC3-硬币之咒.webp" alt=""><span>
                    <h2>硬币之咒</h2>
                    <h3>薛定谔的冠军</h3>
                </span>
            </div>
        </div>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC3-硬币收集.webp" alt=""><span>
                    <h2>硬币收集</h2>
                    <h3>落雪队</h3>
                </span>
            </div>
        </div>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC3-地区贸易.webp" alt=""><span>
                    <h2>地区贸易</h2>
                    <h3>煎蛋的小队</h3>
                </span>
            </div>
        </div>


        <h2>MCC2 <a onclick="" target="_blank" href="https://www.bilibili.com/video/BV1XHvYe8EpC/">照片</a></h2>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC2-红沙发照相馆.webp" alt=""><span>
                    <h2>红沙发照相馆</h2>
                    <h3>16-bit</h3>
                </span>
            </div>
        </div>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC2-梦境摄手.webp" alt=""><span>
                    <h2>梦境摄手</h2>
                    <h3>UNDERLINE</h3>
                </span>
            </div>
        </div>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC2-时光相片.webp" alt=""><span>
                    <h2>时光相片</h2>
                    <h3>不简单的小队</h3>
                </span>
            </div>
        </div>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC2-Photo Scared.webp" alt=""><span>
                    <h2>Photo Scared</h2>
                    <h3>DYM</h3>
                </span>
            </div>
        </div>

        <h2>MCC1 <a onclick="" target="_blank" href="https://www.bilibili.com/video/BV1Qz421R7e7/">种子</a></h2>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC1-大富翁.webp" alt=""><span>
                    <h2>大富翁</h2>
                    <h3>鸽子窝</h3>
                </span>
            </div>
        </div>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC1-种子基因库.webp" alt=""><span>
                    <h2>种子基因库</h2>
                    <h3>無限水</h3>
                </span>
            </div>
        </div>
        <div class="game-box">
            <div>
                <img src="./imgs/MCC1-洞穴之种.webp" alt=""><span>
                    <h2>洞窟之种</h2>
                    <h3>一个单单简简の小队</h3>
                </span>
            </div>
        </div>

        <h2>MCC0 <a onclick="" target="_blank" href="https://www.bilibili.com/video/BV1Ep421f7EL/">倒计时</a></h2>
        <div class="game-box">
            <div>
                <img src="./imgs/健康倒计时.webp" alt=""><span>
                    <h2>健康倒计时</h2>
                    <h3>鸽子窝</h3>
                </span>
            </div>
        </div>
    </child>
'''

import re

a = re.findall('<child id="(.+?)">(.*?)</child>',html,re.DOTALL)
print(a)