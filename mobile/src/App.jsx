import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import EditorScreen from './screens/EditorScreen';
import Viewer3DScreen from './screens/Viewer3DScreen';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Editor" component={EditorScreen} />
        <Tab.Screen name="3D Viewer" component={Viewer3DScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
