<!-- title: 我的世界数据包进阶教程系列 -->
<!-- headimg: ./headimg.png -->
<!-- date: 2023/11/07 -->

<!--
文章标题：我的世界数据包进阶教程系列
作者：孤帆Gufandf
校对：
启动日期：2023年11月7日
资料来源：
- [Minecraft Wiki](https://minecraft.wiki/)
-->


<h1>我的世界数据包进阶教程系列</h1>

[TOC]

# 射线检测

## 导语

射线检测是一种通过发射射线来检测某个方向上方块或者实体的方式。这在一些场景下会经常用到，如确定子弹的命中情况、测量距离、判断玩家视线是否看向某个位置、又或许检测玩家所看的是什么方块。

## 原理详解

射线检测的过程分为以下几步：

1. 发射
2. 步进
3. 判断
4. 循环

在数据包内新建一个名为 ray.mcfunction 的文件，方便我们使用射线检测。

我们需要生成一个帮助我们检测的实体，一般使用 marker，低版本也可以使用隐身的盔甲架。同时，给它他添加一个名为 ray 的标签，方便我们在后面选择它。

```mcfunction
# /ray.mcfunction

summon marker ~ ~ ~ {Tags:["ray"]}
```

将这个 marker 的角度设置为和玩家视角方向相同

```mcfunction
data modify entity @e[tag=ray,limit=1] Rotation set from entity @s Rotation
```

接下来，创建 step.mcfunction 文件， marker 每一次需要步进时都要运行这个函数，在 marker 生成后也需要调用这个函数来开始第一次步进。由此，ray.mcfunction 文件变成了这样。

```mcfunction
# /ray.mcfunction

# 生成
summon marker ~ ~ ~ {Tags:["ray"]}
# 转向
data modify entity @e[tag=ray,limit=1] Rotation set from entity @s Rotation
# 启动第一次步进
execute as @e[tag=ray] at @s run function ray:step
```

步进时， marker 需要前进一小段距离，运行检测程序。如果需要判断的条件不成立，就继续前进，直到条件成立。因此，这个循环被我称为步进。在这一过程中，使用了递归的思想，即在函数内调用本函数来进行循环判断。

```mcfunction
# /step.mcfunction
 
tp @s ^ ^ ^0.1

function ray:step
```

为了避免陷入死循环，射线需要有一个步进次数限制。

```mcfunction
# /load.mcfunction

scoreboard objectives add Raylimit dummy
```

```mcfunction
# 步进次数限制
scoreboard players add @s Raylimit 1
execute if score @s Raylimit matches ..49 run function ray:step
execute if score @s Raylimit matches 50.. run kill @s
```

这样，只有当步数小于一定值时，递归才会进行下去。

当然为了方便以后添加更多提前中断递归的条件（比如检测玩家面向的方块，在碰到方块后就可以结束递归了），在递归需要中断时给 marker 添加一个标签 即可。

```mcfunction
# 步进次数限制
scoreboard players add @s Raylimit 1
execute if score @s Raylimit matches 50.. run tag @s add RayOver
execute if entity @s[tag=!RayOver] run function ray:step
execute if entity @s[tag=RayOver] run kill @s
```

在这里，当步进步数达到 50 时，marker 会给自己添加 RayOver 标签，下一次递归不会运行，本 marker 也会在最后删除。

$$恭喜你成功发射了一条射线！ （虽然它还没有任何功能$$

接下来，我们要添加一些判断条件让这变得更有趣。

```mcfunction
# 条件判断
execute if block ~ ~ ~ grass_block run say this is grass_block!
execute if block ~ ~ ~ grass_block run tag @s add RayOver
```

$$ /execute是非常强大的指令，在判断方面我们有求于他$$

在这条指令中，当 marker 所在方块为草方块时（可以理解为射线和草方块发生了碰撞），marker 会发送一句话，同时给自己添加 RayOver 标签。

由于这两句的判断条件相同，可以考虑把这两行整合进同一个函数。

```mcfunction
# 条件判断
execute if block ~ ~ ~ grass_block run function ray:ray_conditions# /collision_grass_block
```

```mcfunction
# /ray_conditions# /collision_grass_block

say this is grass_block!
tag @s add RayOver
```

在条件判断部分我们还可以加更多的条件进行更复杂的判断。

```mcfunction
execute if entity @e[type=ender_dragon,distance=..10] run function ray:ray_conditions# /kill_the_dragon
```

```mcfunction
# /ray_conditions# /kill_the_dragon

kill @e[type=ender_dragon,sort=nearest,limit=1]
tag @s add RayOver
```

由此，整个 step.mcfunction 变成了这样。

```mcfunction
# /step.mcfunction

tp @s ^ ^ ^0.1

# 条件判断
execute if block ~ ~ ~ grass_block run function ray:ray_conditions# /collision_grass_block
execute if entity @e[type=ender_dragon,distance=..10] run function ray:ray_conditions# /kill_the_dragon

# 步进次数限制
scoreboard players add @s Raylimit 1
execute if score @s Raylimit matches 50.. run tag @s add RayOver
execute if entity @s[tag=!RayOver] run function ray:step
execute if entity @s[tag=RayOver] run kill @s
```

## 实战演练

还没写
