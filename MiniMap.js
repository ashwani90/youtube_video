import React from 'react';
import { View, VrButton, Image, StyleSheet } from 'react-360';

const MiniMap = ({ onSceneChange }) => {
    return (
        <View style={styles.mapContainer}>
            <Image source={{ uri: 'static_assets/map.png' }} style={styles.map} />
            <VrButton style={[styles.hotspot, { left: '20%', top: '50%' }]} onClick={() => onSceneChange('livingRoom')} />
            <VrButton style={[styles.hotspot, { left: '50%', top: '30%' }]} onClick={() => onSceneChange('kitchen')} />
            <VrButton style={[styles.hotspot, { left: '80%', top: '70%' }]} onClick={() => onSceneChange('bedroom')} />
        </View>
    );
};

const styles = StyleSheet.create({
    mapContainer: {
        position: 'absolute',
        right: 20,
        top: 20,
        width: 200,
        height: 200,
        backgroundColor: 'rgba(255, 255, 255, 0.8)',
        borderRadius: 10,
    },
    map: {
        width: '100%',
        height: '100%',
    },
    hotspot: {
        position: 'absolute',
        width: 20,
        height: 20,
        backgroundColor: 'red',
        borderRadius: 10,
    },
});

export default MiniMap;



