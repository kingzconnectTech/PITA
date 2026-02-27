/**
 * PITA Avatar Renderer
 * Handles the Three.js scene, camera, lighting, and 3D avatar animation.
 */

import * as THREE from 'three';
import { State } from './state.js';

export class AvatarRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) {
            console.error(`[Avatar] Canvas with ID "${canvasId}" not found.`);
            return;
        }

        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.avatar = null; // Placeholder for GLTF model
        this.clock = new THREE.Clock();
        
        this.init();
        this.addPlaceholderAvatar();
        this.animate();
        this.handleResize();
    }

    /**
     * Initialize Three.js scene, camera, and renderer
     */
    init() {
        console.log('[Avatar] Initializing Three.js scene...');
        
        // Scene setup
        this.scene = new THREE.Scene();
        // Subtle background color or skybox could go here
        
        // Camera setup
        const aspect = window.innerWidth / window.innerHeight;
        this.camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);
        this.camera.position.z = 5;

        // Renderer setup
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            antialias: true,
            alpha: true // Transparent background
        });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.toneMapping = THREE.ReinhardToneMapping;

        // Lighting setup
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        this.scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0x00f2ff, 1);
        directionalLight.position.set(1, 1, 2);
        this.scene.add(directionalLight);
        
        const secondaryLight = new THREE.PointLight(0x7000ff, 0.8);
        secondaryLight.position.set(-2, -1, 1);
        this.scene.add(secondaryLight);
    }

    /**
     * Add a stylized 3D face structure for the avatar
     */
    addPlaceholderAvatar() {
        console.log('[Avatar] Constructing 3D Face...');
        
        // Group all face components together
        this.avatar = new THREE.Group();
        this.scene.add(this.avatar);

        // 1. Main Head (The Sphere)
        const headGeo = new THREE.IcosahedronGeometry(1.5, 4);
        const headMat = new THREE.MeshStandardMaterial({
            color: 0x00f2ff,
            wireframe: true,
            emissive: 0x00f2ff,
            emissiveIntensity: 0.3,
            transparent: true,
            opacity: 0.4
        });
        this.head = new THREE.Mesh(headGeo, headMat);
        this.avatar.add(this.head);

        // 2. Inner Core (Brain)
        const coreGeo = new THREE.SphereGeometry(0.8, 32, 32);
        const coreMat = new THREE.MeshPhongMaterial({
            color: 0x7000ff,
            emissive: 0x7000ff,
            emissiveIntensity: 0.5,
            transparent: true,
            opacity: 0.8
        });
        this.core = new THREE.Mesh(coreGeo, coreMat);
        this.avatar.add(this.core);

        // 3. Eyes
        const eyeGeo = new THREE.SphereGeometry(0.15, 16, 16);
        const eyeMat = new THREE.MeshStandardMaterial({
            color: 0xffffff,
            emissive: 0xffffff,
            emissiveIntensity: 1.0,
        });

        this.leftEye = new THREE.Mesh(eyeGeo, eyeMat);
        this.leftEye.position.set(-0.5, 0.4, 1.2);
        this.avatar.add(this.leftEye);

        this.rightEye = new THREE.Mesh(eyeGeo, eyeMat);
        this.rightEye.position.set(0.5, 0.4, 1.2);
        this.avatar.add(this.rightEye);

        // 4. Eye Glows (The actual pupils/glowing part)
        const pupilGeo = new THREE.SphereGeometry(0.06, 8, 8);
        const pupilMat = new THREE.MeshBasicMaterial({ color: 0x00f2ff });
        
        const leftPupil = new THREE.Mesh(pupilGeo, pupilMat);
        leftPupil.position.set(0, 0, 0.1);
        this.leftEye.add(leftPupil);

        const rightPupil = new THREE.Mesh(pupilGeo, pupilMat);
        rightPupil.position.set(0, 0, 0.1);
        this.rightEye.add(rightPupil);

        // 5. Mouth (A simple glowing ring/arc)
        const mouthGeo = new THREE.TorusGeometry(0.3, 0.03, 16, 32, Math.PI);
        const mouthMat = new THREE.MeshStandardMaterial({
            color: 0x00f2ff,
            emissive: 0x00f2ff,
            emissiveIntensity: 1.0
        });
        this.mouth = new THREE.Mesh(mouthGeo, mouthMat);
        this.mouth.position.set(0, -0.4, 1.1);
        this.mouth.rotation.x = Math.PI / 2;
        this.avatar.add(this.mouth);
    }

    /**
     * Animation loop
     */
    animate() {
        requestAnimationFrame(() => this.animate());
        
        const elapsedTime = this.clock.getElapsedTime();

        if (this.avatar) {
            // 1. Idle Floating & Subtle Rotation
            this.avatar.position.y = Math.sin(elapsedTime * 1.5) * 0.15;
            this.avatar.rotation.y = Math.sin(elapsedTime * 0.5) * 0.1;
            this.avatar.rotation.x = Math.cos(elapsedTime * 0.3) * 0.05;

            // 2. Eye Blinking (Randomly every few seconds)
            const blinkFrequency = 4.0;
            const blinkDuration = 0.15;
            const isBlinking = (elapsedTime % blinkFrequency) < blinkDuration;
            
            if (this.leftEye && this.rightEye) {
                const eyeScale = isBlinking ? 0.1 : 1.0;
                this.leftEye.scale.y = THREE.MathUtils.lerp(this.leftEye.scale.y, eyeScale, 0.2);
                this.rightEye.scale.y = THREE.MathUtils.lerp(this.rightEye.scale.y, eyeScale, 0.2);
            }

            // 3. React to status
            switch (State.status) {
                case 'listening':
                    // Head "tilts" to listen and eyes pulse green
                    this.avatar.rotation.z = Math.sin(elapsedTime * 5) * 0.05;
                    this.updateColors(0x00ff88); // Green (Listening)
                    this.leftEye.scale.setScalar(1.2 + Math.sin(elapsedTime * 10) * 0.1);
                    this.rightEye.scale.setScalar(1.2 + Math.sin(elapsedTime * 10) * 0.1);
                    break;
                case 'processing':
                    // Rapid core spinning
                    if (this.core) this.core.rotation.y += 0.2;
                    this.updateColors(0xff8800); // Orange (Processing)
                    break;
                case 'speaking':
                    // Mouth movement (syncing with "speech")
                    if (this.mouth) {
                        const mouthScale = 1.0 + Math.abs(Math.sin(elapsedTime * 12)) * 0.5;
                        this.mouth.scale.set(mouthScale, mouthScale, 1);
                    }
                    this.updateColors(0x7000ff); // Purple (Speaking)
                    break;
                default: // 'idle'
                    this.updateColors(0x00f2ff); // Blue (Idle/Wake)
                    if (this.mouth) this.mouth.scale.set(1, 1, 1);
            }
        }

        this.renderer.render(this.scene, this.camera);
    }

    /**
     * Helper to update emissive colors of face components
     * @param {number} hexColor 
     */
    updateColors(hexColor) {
        if (!this.head || !this.mouth) return;
        this.head.material.color.setHex(hexColor);
        this.head.material.emissive.setHex(hexColor);
        this.mouth.material.color.setHex(hexColor);
        this.mouth.material.emissive.setHex(hexColor);
    }

    /**
     * Handle window resizing
     */
    handleResize() {
        window.addEventListener('resize', () => {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(window.innerWidth, window.innerHeight);
        });
    }

    /**
     * Load a real GLTF model (placeholder for future use)
     * @param {string} url 
     */
    async loadModel(url) {
        // This will require GLTFLoader from Three.js examples
        console.log(`[Avatar] Loading model from: ${url}`);
        // Implementation for future
    }
}
