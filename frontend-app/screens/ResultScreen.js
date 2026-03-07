import React from 'react';
import { View, Text, StyleSheet, ScrollView, Image, Alert } from 'react-native';
import { useRoute } from '@react-navigation/native';
import Card from '../components/Card';
import Button from '../components/Button';

const ResultScreen = () => {
  const route = useRoute();
  const { result, imageUri } = route.params || {};

  if (!result) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>No result data available</Text>
      </View>
    );
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#4CAF50';
    if (confidence >= 0.6) return '#FF9800';
    return '#F44336';
  };

  const getConfidenceText = (confidence) => {
    if (confidence >= 0.8) return 'High Confidence';
    if (confidence >= 0.6) return 'Medium Confidence';
    return 'Low Confidence';
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.imageContainer}>
        <Image source={{ uri: imageUri }} style={styles.scannedImage} />
        <View style={styles.confidenceBadge}>
          <Text style={[
            styles.confidenceText,
            { color: getConfidenceColor(result.confidence) }
          ]}>
            {Math.round(result.confidence * 100)}% - {getConfidenceText(result.confidence)}
          </Text>
        </View>
      </View>

      <Card title="Disease Detection Result">
        <View style={styles.resultItem}>
          <Text style={styles.resultLabel}>Detected Disease:</Text>
          <Text style={styles.resultValue}>{result.disease || 'Unknown'}</Text>
        </View>
      </Card>

      <Card title="Treatment Recommendations">
        <View style={styles.treatmentSection}>
          <Text style={styles.treatmentTitle}>🧪 Medicine</Text>
          <Text style={styles.treatmentContent}>{result.medicine || 'Not available'}</Text>
        </View>

        <View style={styles.treatmentSection}>
          <Text style={styles.treatmentTitle}>🌱 Fertilizer</Text>
          <Text style={styles.treatmentContent}>{result.fertilizer || 'Not available'}</Text>
        </View>

        <View style={styles.treatmentSection}>
          <Text style={styles.treatmentTitle}>💡 Tips</Text>
          <Text style={styles.treatmentContent}>{result.tips || 'Not available'}</Text>
        </View>
      </Card>

      {result.error && (
        <Card title="Note">
          <Text style={styles.errorText}>{result.error}</Text>
        </Card>
      )}

      <View style={styles.actionButtons}>
        <Button
          title="Scan Another Crop"
          onPress={() => {
            // Navigate back to scan screen
            // navigation.navigate('Scan');
          }}
          style={styles.actionButton}
        />
        <Button
          title="Save Result"
          onPress={() => {
            Alert.alert('Success', 'Result saved to your history');
          }}
          style={styles.actionButton}
        />
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  imageContainer: {
    position: 'relative',
    backgroundColor: '#000',
    height: 250,
  },
  scannedImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'contain',
  },
  confidenceBadge: {
    position: 'absolute',
    top: 10,
    right: 10,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    padding: 8,
    borderRadius: 5,
  },
  confidenceText: {
    fontSize: 12,
    fontWeight: 'bold',
  },
  resultItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
  },
  resultLabel: {
    fontSize: 16,
    color: '#666',
    fontWeight: '500',
  },
  resultValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
    textAlign: 'right',
  },
  treatmentSection: {
    marginBottom: 20,
  },
  treatmentTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#333',
  },
  treatmentContent: {
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
  },
  errorText: {
    color: '#F44336',
    fontSize: 14,
  },
  actionButtons: {
    padding: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  actionButton: {
    flex: 1,
    marginHorizontal: 5,
  },
});

export default ResultScreen;
