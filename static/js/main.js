document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate');
    const saveImageBtn = document.getElementById('save-image');
    const recipientInput = document.getElementById('recipient');
    const requirementsInput = document.getElementById('requirements');
    const resultSection = document.querySelector('.result-section');
    const greetingText = document.getElementById('greeting-text');
    const coupletContainer = document.getElementById('couplet-container');
    const historyList = document.getElementById('history-list');
    const loading = document.getElementById('loading');

    // 本地存储相关函数
    const saveToHistory = (data) => {
        try {
            const history = JSON.parse(localStorage.getItem('greetings_history') || '[]');
            history.unshift(data);
            // 只保留最近10条记录
            history.splice(10);
            localStorage.setItem('greetings_history', JSON.stringify(history));
        } catch (error) {
            console.error('保存历史记录失败:', error);
        }
    };

    const getHistory = () => {
        try {
            return JSON.parse(localStorage.getItem('greetings_history') || '[]');
        } catch (error) {
            console.error('获取历史记录失败:', error);
            return [];
        }
    };

    // 移动端触摸反馈
    const addTouchFeedback = (element) => {
        element.addEventListener('touchstart', () => {
            element.style.opacity = '0.8';
        }, { passive: true });

        element.addEventListener('touchend', () => {
            element.style.opacity = '1';
        }, { passive: true });
    };

    // 为按钮添加触摸反馈
    [generateBtn, saveImageBtn].forEach(addTouchFeedback);

    // 自动调整文本框高度
    requirementsInput.addEventListener('input', () => {
        requirementsInput.style.height = 'auto';
        requirementsInput.style.height = (requirementsInput.scrollHeight) + 'px';
    });

    // 在移动端输入完成后自动隐藏键盘
    recipientInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
            recipientInput.blur();
        }
    });

    // 加载历史记录
    function loadHistory() {
        const history = getHistory();
        historyList.innerHTML = '';
        
        history.forEach((item, index) => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            historyItem.style.animation = `fadeIn 0.5s ease-out ${index * 0.1}s forwards`;
            historyItem.style.opacity = '0';
            
            historyItem.innerHTML = `
                <div class="history-header">
                    <strong>${item.recipient}</strong>
                    <span class="history-time">${new Date(item.timestamp).toLocaleString()}</span>
                </div>
                <div class="history-content">
                    <p class="greeting">${item.greeting}</p>
                    <div class="couplet-text">
                        <p class="horizontal">横批：${item.couplet.horizontal}</p>
                        <p class="upper">上联：${item.couplet.upper}</p>
                        <p class="lower">下联：${item.couplet.lower}</p>
                    </div>
                </div>
            `;
            
            historyList.appendChild(historyItem);
        });

        // 如果没有历史记录，显示提示
        if (history.length === 0) {
            historyList.innerHTML = '<div class="no-history">暂无历史记录</div>';
        }
    }

    // 生成祝福
    generateBtn.addEventListener('click', async () => {
        const recipient = recipientInput.value.trim();
        const requirements = requirementsInput.value.trim();

        if (!recipient) {
            alert('请输入接收祝福的人的名字');
            recipientInput.focus();
            return;
        }

        try {
            loading.style.display = 'flex';
            // 在移动端生成时收起键盘
            if (window.innerWidth <= 768) {
                document.activeElement.blur();
            }

            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    recipient,
                    requirements
                })
            });

            if (!response.ok) {
                throw new Error('请重试');
            }

            const data = await response.json();
            
            // 保存到本地存储
            saveToHistory({
                recipient,
                greeting: data.greeting,
                couplet: data.couplet,
                timestamp: data.timestamp
            });

            // 显示结果
            greetingText.textContent = data.greeting;
            coupletContainer.innerHTML = `<img src="data:image/png;base64,${data.image}" alt="春联">`;
            resultSection.style.display = 'block';
            
            // 平滑滚动到结果区域
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

            // 刷新历史记录
            loadHistory();
        } catch (error) {
            alert('生成失败: ' + error.message);
        } finally {
            loading.style.display = 'none';
        }
    });

    // 保存图片
    saveImageBtn.addEventListener('click', () => {
        const image = coupletContainer.querySelector('img');
        if (image) {
            // 检查是否为移动设备
            const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
            
            if (isMobile) {
                // 在新标签页中打开图片，用户可以长按保存
                window.open(image.src, '_blank');
            } else {
                // 桌面端使用下载方式
                const link = document.createElement('a');
                link.download = '春联.png';
                link.href = image.src;
                link.click();
            }
        }
    });

    // 初始加载历史记录
    loadHistory();

    // 添加页面可见性变化处理
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
            loadHistory();
        }
    });
}); 