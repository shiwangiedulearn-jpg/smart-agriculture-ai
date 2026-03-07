import React, { useState, useRef } from 'react';
import { View, Text, StyleSheet, Alert, TouchableOpacity, Image } from 'react-native';
import { Camera } from 'expo-camera';
import { useNavigation } from '@react-navigation/native';
import Button from '../components/Button';
import { predictDisease } from '../services/api';

const ScanScreen = () => {
  const [hasPermission, setHasPermission] = useState(null);
  const [cameraActive, setCameraActive] = useState(true);
  const [loading, setLoading] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const cameraRef = useRef();
  const navigation = useNavigation();

  React.useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const takePicture = async () => {
    if (cameraRef.current) {
      try {
        const photo = await cameraRef.current.takePictureAsync({
          quality: 0.7,
          base64: false,
        });
        setCapturedImage(photo);
        setCameraActive(false);
      } catch (error) {
        Alert.alert('Error', 'Failed to take picture');
      }
    }
  };

  const analyzeImage = async () => {
    if (!capturedImage) return;

    setLoading(true);
    try {
      const result = await predictDisease(capturedImage.uri);
      navigation.navigate('Result', { result, imageUri: capturedImage.uri });
    } catch (error) {
      Alert.alert('Error', error.detail || 'Failed to analyze image');
    } finally {
      setLoading(false);
    }
  };

  const retakePicture = () => {
    setCapturedImage(null);
    setCameraActive(true);
  };

  if (hasPermission === null) {
    return (
      <View style={styles.container}>
        <Text>Requesting camera permission...</Text>
      </View>
    );
  }

  if (hasPermission === false) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>No access to camera</Text>
        <Text>Please enable camera permissions to use this feature</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Scan Crop Disease</Text>
      
      {cameraActive ? (
        <View style={styles.cameraContainer}>
          <Camera
            ref={cameraRef}
            style={styles.camera}
            type={Camera.Constants.Type.back}
            autoFocus={Camera.Constants.AutoFocus.on}
          />
          <View style={styles.cameraOverlay}>
            <View style={styles.focusFrame} />
            <Text style={styles.instructionText}>
              Position the leaf within the frame
            </Text>
          </View>
        </View>
      ) : (
        <View style={styles.previewContainer}>
          <Image source={{ uri: capturedImage.uri }} style={styles.preview} />
        </View>
      )}

      <View style={styles.buttonContainer}>
        {cameraActive ? (
          <TouchableOpacity style={styles.captureButton} onPress={takePicture}>
            <View style={styles.captureButtonInner} />
          </TouchableOpacity>
        ) : (
          <>
            <Button
              title="Retake"
              onPress={retakePicture}
              style={styles.retakeButton}
            />
            <Button
              title={loading ? 'Analyzing...' : 'Analyze'}
              onPress={analyzeImage}
              disabled={loading}
              style={styles.analyzeButton}
            />
          </>
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  title: {
    position: 'absolute',
    top: 50,
    left: 0,
    right: 0,
    textAlign: 'center',
    color: 'white',
    fontSize: 20,
    fontWeight: 'bold',
    zIndex: 10,
  },
  cameraContainer: {
    flex: 1,
  },
  camera: {
    flex: 1,
  },
  cameraOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
  },
  focusFrame: {
    width: 250,
    height: 250,
    borderWidth: 2,
    borderColor: '#4CAF50',
    borderRadius: 8,
    backgroundColor: 'transparent',
  },
  instructionText: {
    position: 'absolute',
    bottom: 100,
    color: 'white',
    fontSize: 16,
    backgroundColor: 'rgba(0,0,0,0.7)',
    padding: 10,
    borderRadius: 5,
  },
  previewContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  preview: {
    width: '100%',
    height: '70%',
    resizeMode: 'contain',
  },
  buttonContainer: {
    position: 'absolute',
    bottom: 50,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  captureButton: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: 'white',
    justifyContent: 'center',
    alignItems: 'center',
  },
  captureButtonInner: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#ff0000',
  },
  retakeButton: {
    backgroundColor: '#FF9800',
    marginRight: 10,
    flex: 1,
  },
  analyzeButton: {
    backgroundColor: '#4CAF50',
    marginLeft: 10,
    flex: 1,
  },
  errorText: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
});

export default ScanScreen;
