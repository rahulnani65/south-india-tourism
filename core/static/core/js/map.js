const container = document.getElementById('map-container');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

camera.position.z = 5;

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
directionalLight.position.set(0, 1, 1);
scene.add(directionalLight);

const loader = new THREE.SVGLoader();
loader.load('{% static "core/images/india.svg" %}', (data) => {
    const paths = data.paths;
    const stateMeshes = [];

    paths.forEach((path) => {
        const id = path.userData.node.id;
        if (stateData[id]) {
            const stateInfo = stateData[id];
            const shapes = path.toShapes(true);
            shapes.forEach((shape) => {
                const geometry = new THREE.ExtrudeGeometry(shape, { depth: 0.1, bevelEnabled: false });
                const material = new THREE.MeshPhongMaterial({ color: getColorForState(id) });
                const mesh = new THREE.Mesh(geometry, material);
                mesh.userData = { name: stateInfo.name, url: stateInfo.url };
                scene.add(mesh);
                stateMeshes.push(mesh);

                addLabel(stateInfo.name, mesh.position);
            });
        }
    });

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    function onMouseClick(event) {
        const rect = renderer.domElement.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(stateMeshes);
        if (intersects.length > 0) {
            const state = intersects[0].object.userData;
            window.location.href = state.url;
        }
    }

    window.addEventListener('click', onMouseClick);
});

function getColorForState(id) {
    const colors = {
        'IN-KL': 0x00ff00,  // Green for Kerala
        'IN-KA': 0xff0000,  // Red for Karnataka
        'IN-TN': 0x0000ff,  // Blue for Tamil Nadu
        'IN-AP': 0xffff00,  // Yellow for Andhra Pradesh
        'IN-TG': 0xff00ff   // Magenta for Telangana
    };
    return colors[id] || 0xcccccc;
}

function addLabel(text, position) {
    const canvas = document.createElement('canvas');
    canvas.width = 128;
    canvas.height = 32;
    const context = canvas.getContext('2d');
    context.font = 'Bold 20px Arial';
    context.fillStyle = 'white';
    context.fillText(text, 0, 20);

    const texture = new THREE.Texture(canvas);
    texture.needsUpdate = true;

    const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
    const sprite = new THREE.Sprite(spriteMaterial);
    sprite.scale.set(1, 0.5, 1);
    sprite.position.set(position.x, position.y + 0.2, position.z);
    scene.add(sprite);
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
});