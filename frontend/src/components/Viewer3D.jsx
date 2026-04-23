import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

export const Viewer3D = ({ gcode }) => {
  const containerRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const rendererRef = useRef(null);
  const controlsRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);
    const camera = new THREE.PerspectiveCamera(45, containerRef.current.clientWidth / containerRef.current.clientHeight, 0.1, 1000);
    camera.position.set(100, 100, 100);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight);
    containerRef.current.appendChild(renderer.domElement);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    const ambientLight = new THREE.AmbientLight(0x404060);
    scene.add(ambientLight);
    const dirLight = new THREE.DirectionalLight(0xffffff, 1);
    dirLight.position.set(50, 100, 50);
    scene.add(dirLight);
    const gridHelper = new THREE.GridHelper(200, 20, 0x888888, 0xcccccc);
    scene.add(gridHelper);

    sceneRef.current = scene;
    cameraRef.current = camera;
    rendererRef.current = renderer;
    controlsRef.current = controls;

    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      const width = containerRef.current.clientWidth;
      const height = containerRef.current.clientHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      containerRef.current?.removeChild(renderer.domElement);
      renderer.dispose();
    };
  }, []);

  useEffect(() => {
    if (!sceneRef.current || !gcode) return;
    const points = parseGcodeToPoints(gcode);
    if (points.length === 0) return;
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({ color: 0xff6600 });
    const pathLine = new THREE.Line(geometry, material);
    sceneRef.current.add(pathLine);
    return () => sceneRef.current?.remove(pathLine);
  }, [gcode]);

  function parseGcodeToPoints(gcodeStr) {
    const points = [];
    let x = 0, y = 0, z = 0;
    const lines = gcodeStr.split('\n');
    for (const line of lines) {
      const xm = line.match(/X([\d.-]+)/);
      const ym = line.match(/Y([\d.-]+)/);
      const zm = line.match(/Z([\d.-]+)/);
      if (xm) x = parseFloat(xm[1]);
      if (ym) y = parseFloat(ym[1]);
      if (zm) z = parseFloat(zm[1]);
      if (xm || ym || zm) points.push(new THREE.Vector3(x, y, z));
    }
    return points;
  }

  return <div ref={containerRef} style={{ width: '100%', height: '500px' }} />;
};
