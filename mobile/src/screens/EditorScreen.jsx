import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';

export default function EditorScreen() {
  const [gcode, setGcode] = useState('');
  return (
    <View style={styles.container}>
      <Text>Editor G-code</Text>
      <TextInput
        multiline
        style={styles.input}
        value={gcode}
        onChangeText={setGcode}
        placeholder="Cole seu G-code aqui"
      />
      <Button title="Processar" onPress={() => alert('Processado localmente')} />
    </View>
  );
}
const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  input: { height: 200, borderColor: 'gray', borderWidth: 1, marginVertical: 10, padding: 10 },
});
