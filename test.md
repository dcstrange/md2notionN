岭回归（Ridge Regression）是另一种常用的正则化线性回归方法。与Lasso回归不同，岭回归使用L2正则化项。具体地说，岭回归的目标函数是：

$$
\text{minimize} \quad ||Y - X\beta||_2^2 + \lambda ||\beta||_2^2
$$

其中，$Y$ 是响应变量，$X$ 是特征矩阵，$\beta$ 是回归系数，$\lambda$ 是正则化参数，$||\cdot||_2$ 是L2范数（欧几里得范数）。

在二维空间中，L2正则化项形成一个圆形区域。我将绘制岭回归的正则化项和损失函数的等高线图，以及它们的组合。

上面的图展示了两种等高线图，与之前的Lasso回归可视化相对应：

1. **左图**：表示岭回归（Ridge Regression）的L2正则化项的等高线。在这里，我们只可视化了正则化项 $ \lambda (\beta_1^2 + \beta_2^2) $。
2. **右图**：表示岭回归的组合目标函数（即损失项和正则化项之和）的等高线。

与Lasso回归不同，岭回归的L2正则化项形成一个圆形区域（左图）。在组合目标函数中（右图），最优解通常会出现在圆形区域和凸抛物面的交点处。

需要注意的是，岭回归不会将回归系数压缩为零，但会使它们尽可能小。这就是为什么在右图中，最优解通常不会出现在轴上，而是在接近原点的区域内。这与Lasso回归形成鲜明对比，后者倾向于产生稀疏解。

