// main.js - Terminal Theme Core
(function() {
    'use strict';
    
    // Load and apply config
    async function loadConfig() {
        try {
            const res = await fetch('config.json');
            return await res.json();
        } catch(e) {
            return null; // Falls back to HTML defaults
        }
    }
    
    // Mobile menu toggle
    window.toggleMenu = function() {
        const menu = document.getElementById('mobile-menu');
        const icon = document.getElementById('menu-icon');
        const toggle = document.querySelector('.mobile-toggle');
        if (!menu || !icon) return;
        menu.classList.toggle('open');
        const isOpen = menu.classList.contains('open');
        icon.className = isOpen ? 'fas fa-times' : 'fas fa-bars';
        if (toggle) toggle.setAttribute('aria-expanded', isOpen);
    };
    
    // Nav scroll
    window.addEventListener('scroll', () => {
        const nav = document.getElementById('nav');
        if (nav) nav.classList.toggle('scrolled', window.scrollY > 20);
    });
    
    // Scroll animations with IntersectionObserver
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));
    });
    
    // Re-export observer for dynamically added elements
    window.__themeObserver = observer;
    
    // Smooth scroll for anchors
    document.addEventListener('click', (e) => {
        const anchor = e.target.closest('a[href^="#"]');
        if (!anchor) return;
        e.preventDefault();
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    
    // Matrix Rain
    (function initMatrix() {
        const canvas = document.getElementById('matrix-bg');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let w, h, columns, drops;
        const chars = '01{}[]()<>/\\|;:=+-*&^%$#@!~`abcdef0123456789ABCDEF';
        
        function resize() {
            w = canvas.width = window.innerWidth;
            h = canvas.height = window.innerHeight;
            columns = Math.floor(w / 14);
            drops = Array(columns).fill(1);
        }
        
        function draw() {
            ctx.fillStyle = 'rgba(10, 14, 23, 0.06)';
            ctx.fillRect(0, 0, w, h);
            ctx.fillStyle = '#4ade80';
            ctx.font = '14px JetBrains Mono, monospace';
            for (let i = 0; i < drops.length; i++) {
                const char = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(char, i * 14, drops[i] * 14);
                if (drops[i] * 14 > h && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        
        // Respect reduced motion
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
        resize();
        window.addEventListener('resize', resize);
        setInterval(draw, 50);
    })();
})();
