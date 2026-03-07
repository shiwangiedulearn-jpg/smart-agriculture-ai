import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import Button from '../components/Button';
import Card from '../components/Card';

const HomeScreen = () => {
  const navigation = useNavigation();

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Smart Agriculture AI</Text>
        <Text style={styles.subtitle}>Your farming companion</Text>
      </View>

      <Card title="Services">
        <Button
          title="🔍 Scan Crop"
          onPress={() => navigation.navigate('Scan')}
          style={styles.featureButton}
        />
        
        <Button
          title="🌾 Sell Crop"
          onPress={() => navigation.navigate('SellCrop')}
          style={styles.featureButton}
        />
        
        <Button
          title="🛒 Buy Crops"
          onPress={() => navigation.navigate('BuyCrop')}
          style={styles.featureButton}
        />
      </Card>

      <Card title="Quick Stats">
        <View style={styles.statRow}>
          <Text style={styles.statLabel}>Crops Scanned Today</Text>
          <Text style={styles.statValue}>12</Text>
        </View>
        <View style={styles.statRow}>
          <Text style={styles.statLabel}>Active Listings</Text>
          <Text style={styles.statValue}>8</Text>
        </View>
        <View style={styles.statRow}>
          <Text style={styles.statLabel}>Market Price Trend</Text>
          <Text style={styles.statValue}>📈 Rising</Text>
        </View>
      </Card>

      <Card title="Recent Activity">
        <Text style={styles.activityItem}>• Tomato disease detected - Early Blight</Text>
        <Text style={styles.activityItem}>• Sold 50kg of organic tomatoes</Text>
        <Text style={styles.activityItem}>• Bought fresh potatoes from local farm</Text>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 20,
    alignItems: 'center',
    backgroundColor: '#4CAF50',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
    color: 'white',
    opacity: 0.9,
  },
  featureButton: {
    marginBottom: 15,
    backgroundColor: '#2196F3',
  },
  statRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  statLabel: {
    fontSize: 16,
    color: '#666',
  },
  statValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  activityItem: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    paddingLeft: 10,
  },
});

export default HomeScreen;
