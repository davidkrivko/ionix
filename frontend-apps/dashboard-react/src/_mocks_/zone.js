const zones = [
  {
    id: 1,
    name: 'Zone1',
    item: [
      {
        id: 1,
        name: 'BEDROOM',
        point: 79,
        sensorTemp: 86,
        status: 'offline',
        controller: 'IONIQ_CONTROLLER_TEST'
      }
    ]
  },
  {
    id: 2,
    name: 'Zone2',
    item: [
      {
        id: 1,
        name: 'ALEX_HOME_TEST',
        point: 67,
        sensorTemp: 72,
        status: 'online',
        controller: 'IONIQ_CTR_HOME_TEST'
      },
      {
        id: 2,
        name: 'NOT_WORKING_MY_TEST',
        point: 66,
        sensorTemp: 85,
        status: 'offline',
        controller: 'IONIQ_TEST_PAIR_CTR'
      },
      {
        id: 3,
        name: 'NOT_WORKING_KITCHEN',
        point: 61,
        sensorTemp: 72,
        status: 'online',
        controller: 'IONIQ_CONTROLLER_TEST2'
      }
    ]
  }
];
export default zones;
