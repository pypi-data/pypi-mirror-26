GETAccounts_response = {'accounts': [{'id': '123-123-1234567-123', 'tags': []}]}

GETAccountID_response = {
    'account': {'id': '123-123-1234567-123', 'createdTime': '2017-08-11T15:04:31.639182352Z', 'currency': 'AUD',
                'createdByUserID': 6557245, 'alias': 'Primary', 'marginRate': '0.02', 'hedgingEnabled': False,
                'lastTransactionID': '14', 'balance': '99999.9138', 'openTradeCount': 0, 'openPositionCount': 0,
                'pendingOrderCount': 0, 'pl': '-0.0769', 'resettablePL': '-0.0769', 'financing': '-0.0093',
                'commission': '0.0', 'orders': [], 'positions': [{'instrument': 'EUR_USD',
                                                                  'long': {'units': '0.0', 'pl': '-0.0769',
                                                                           'resettablePL': '-0.0769',
                                                                           'financing': '-0.0093',
                                                                           'unrealizedPL': '0.0'},
                                                                  'short': {'units': '0.0', 'pl': '0.0',
                                                                            'resettablePL': '0.0',
                                                                            'financing': '0.0',
                                                                            'unrealizedPL': '0.0'},
                                                                  'pl': '-0.0769', 'resettablePL': '-0.0769',
                                                                  'financing': '-0.0093', 'commission': '0.0',
                                                                  'unrealizedPL': '0.0'}], 'trades': [],
                'unrealizedPL': '0.0', 'NAV': '99999.9138', 'marginUsed': '0.0', 'marginAvailable': '99999.9138',
                'positionValue': '0.0', 'marginCloseoutUnrealizedPL': '0.0', 'marginCloseoutNAV': '99999.9138',
                'marginCloseoutMarginUsed': '0.0', 'marginCloseoutPositionValue': '0.0',
                'marginCloseoutPercent': '0.0', 'withdrawalLimit': '99999.9138', 'marginCallMarginUsed': '0.0',
                'marginCallPercent': '0.0'}, 'lastTransactionID': '14'}

GETAccountIDSummary_response = {
    'account': {'id': '123-123-1234567-123', 'createdTime': '2017-08-11T15:04:31.639182352Z', 'currency': 'AUD',
                'createdByUserID': 6557245, 'alias': 'Primary', 'marginRate': '0.02', 'hedgingEnabled': False,
                'lastTransactionID': '56', 'balance': '100000.1795', 'openTradeCount': 2, 'openPositionCount': 1,
                'pendingOrderCount': 0, 'pl': '0.1899', 'resettablePL': '0.1899', 'financing': '-0.0104',
                'commission': '0.0', 'unrealizedPL': '0.0033', 'NAV': '100000.1828', 'marginUsed': '0.0401',
                'marginAvailable': '100000.1427', 'positionValue': '2.0027', 'marginCloseoutUnrealizedPL': '0.0046',
                'marginCloseoutNAV': '100000.1841', 'marginCloseoutMarginUsed': '0.04',
                'marginCloseoutPositionValue': '2.0', 'marginCloseoutPercent': '0.0',
                'withdrawalLimit': '100000.1427', 'marginCallMarginUsed': '0.04', 'marginCallPercent': '0.0'},
    'lastTransactionID': '56'}

account_changes_transactions_data = [
    {'type': 'MARKET_ORDER', 'instrument': 'AUD_USD', 'units': '-100000', 'timeInForce': 'FOK',
     'positionFill': 'REDUCE_ONLY', 'reason': 'TRADE_CLOSE',
     'tradeClose': {'units': 'ALL', 'tradeID': '70'}, 'id': '73', 'userID': 6557245,
     'accountID': '123-123-1234567-123', 'batchID': '73', 'requestID': '24332661887306834',
     'time': '2017-09-26T02:02:56.859197224Z'},
    {'type': 'ORDER_FILL', 'orderID': '73', 'instrument': 'AUD_USD', 'units': '-100000',
     'price': '0.79411', 'pl': '73.0267', 'financing': '-0.0129', 'commission': '0.0',
     'accountBalance': '100073.1945', 'reason': 'MARKET_ORDER_TRADE_CLOSE', 'tradesClosed': [
        {'tradeID': '70', 'units': '-100000', 'realizedPL': '73.0267', 'financing': '-0.0129'}],
     'fullPrice': {'closeoutBid': '0.79396', 'closeoutAsk': '0.79438',
                   'timestamp': '2017-09-26T02:01:48.859685266Z',
                   'bids': [{'price': '0.79411', 'liquidity': '10000000'}],
                   'asks': [{'price': '0.79423', 'liquidity': '10000000'}]}, 'id': '74',
     'userID': 6557245, 'accountID': '123-123-1234567-123', 'batchID': '73',
     'requestID': '24332661887306834', 'time': '2017-09-26T02:02:56.859197224Z'},
    {'type': 'ORDER_CANCEL', 'orderID': '71', 'reason': 'LINKED_TRADE_CLOSED', 'closedTradeID': '70',
     'tradeCloseTransactionID': '74', 'id': '75', 'userID': 6557245,
     'accountID': '123-123-1234567-123', 'batchID': '73', 'requestID': '24332661887306834',
     'time': '2017-09-26T02:02:56.859197224Z'},
    {'type': 'ORDER_CANCEL', 'orderID': '72', 'reason': 'LINKED_TRADE_CLOSED', 'closedTradeID': '70',
     'tradeCloseTransactionID': '74', 'id': '76', 'userID': 6557245,
     'accountID': '123-123-1234567-123', 'batchID': '73', 'requestID': '24332661887306834',
     'time': '2017-09-26T02:02:56.859197224Z'},
    {'type': 'MARKET_ORDER', 'instrument': 'AUD_USD', 'units': '10000', 'timeInForce': 'FOK',
     'positionFill': 'DEFAULT', 'takeProfitOnFill': {'price': '0.79823', 'timeInForce': 'GTC'},
     'stopLossOnFill': {'price': '0.79273', 'timeInForce': 'GTC'}, 'reason': 'CLIENT_ORDER',
     'id': '77', 'userID': 6557245, 'accountID': '123-123-1234567-123', 'batchID': '77',
     'requestID': '24332662021610694', 'time': '2017-09-26T02:03:28.339330227Z'},
    {'type': 'ORDER_FILL', 'orderID': '77', 'instrument': 'AUD_USD', 'units': '10000',
     'price': '0.79423', 'pl': '0.0', 'financing': '0.0', 'commission': '0.0',
     'accountBalance': '100073.1945', 'reason': 'MARKET_ORDER',
     'tradeOpened': {'tradeID': '78', 'units': '10000'},
     'fullPrice': {'closeoutBid': '0.79394', 'closeoutAsk': '0.79438',
                   'timestamp': '2017-09-26T02:03:08.951115776Z',
                   'bids': [{'price': '0.79409', 'liquidity': '10000000'}],
                   'asks': [{'price': '0.79423', 'liquidity': '10000000'}]}, 'id': '78',
     'userID': 6557245, 'accountID': '123-123-1234567-123', 'batchID': '77',
     'requestID': '24332662021610694', 'time': '2017-09-26T02:03:28.339330227Z'},
    {'type': 'TAKE_PROFIT_ORDER', 'tradeID': '78', 'timeInForce': 'GTC',
     'triggerCondition': 'DEFAULT', 'price': '0.79823', 'reason': 'ON_FILL', 'id': '79',
     'userID': 6557245, 'accountID': '123-123-1234567-123', 'batchID': '77',
     'requestID': '24332662021610694', 'time': '2017-09-26T02:03:28.339330227Z'},
    {'type': 'STOP_LOSS_ORDER', 'tradeID': '78', 'timeInForce': 'GTC', 'triggerCondition': 'DEFAULT',
     'price': '0.79273', 'reason': 'ON_FILL', 'id': '80', 'userID': 6557245,
     'accountID': '123-123-1234567-123', 'batchID': '77', 'requestID': '24332662021610694',
     'time': '2017-09-26T02:03:28.339330227Z'}]

GETInstrumentsCandles_response = {'instrument': 'AUD_USD', 'granularity': 'S5', 'candles': [
    {'time': '1506709800.000000000', 'mid': {'o': '0.78426', 'h': '0.7843', 'l': '0.78426', 'c': '0.7843'}, 'volume': 2,
     'complete': True},
    {'time': '1506709810.000000000', 'mid': {'o': '0.78434', 'h': '0.78438', 'l': '0.78434', 'c': '0.78438'},
     'volume': 2, 'complete': True},
    {'time': '1506709835.000000000', 'mid': {'o': '0.78441', 'h': '0.78448', 'l': '0.78441', 'c': '0.78448'},
     'volume': 3, 'complete': True},
    {'time': '1506709880.000000000', 'mid': {'o': '0.78445', 'h': '0.7845', 'l': '0.78445', 'c': '0.7845'}, 'volume': 2,
     'complete': True}]}

position_response = {'instrument': 'AUD_USD', 'pl': -1290.1203, 'unrealizedPL': -0.0219, 'resettablePL': -1290.1203,
                     'commission': 0.0,
                     'long': {'units': 12.0, 'averagePrice': 0.77079, 'tradeIDs': [4853, 4855, 4857], 'pl': -1086.1652,
                              'unrealizedPL': -0.0219, 'resettablePL': -1086.1652, 'financing': -1.4693},
                     'short': {'units': 0.0, 'pl': -203.9551, 'unrealizedPL': 0.0, 'resettablePL': -203.9551,
                               'financing': -0.643}, 'financing': -2.1123}

order_cancel_transaction_json_dict = {'type': 'ORDER_CANCEL', 'orderID': '4934', 'reason': 'MARKET_HALTED',
                                      'id': '4935', 'userID': 6557245, 'accountID': '123-123-1234567-123',
                                      'batchID': '4934', 'requestID': '42361333491077232',
                                      'time': '1509794347.333636884'}

account_changes_chnages_response = '{"ordersCreated":[],"ordersCancelled":[],"ordersFilled":[{"id":4955,"createTime":"1510528065.059959057","state":"FILLED","type":"MARKET","timeInForce":"FOK","fillingTransactionID":"4956","filledTime":"1510528065.059959057","tradeOpenedID":4956,"instrument":"AUD_JPY","units":"1.0","positionFill":"DEFAULT"}],"ordersTriggered":[],"tradesOpened":[{"id":4956,"instrument":"AUD_JPY","price":"86.918","openTime":"1510528065.059959057","state":"OPEN","initialUnits":"1.0","currentUnits":"1.0","realizedPL":"0.0","financing":"0.0"}],"tradesReduced":[],"tradesClosed":[],"positions":[{"instrument":"AUD_JPY","pl":"-0.0005","resettablePL":"-0.0005","commission":"0.0","long":{"units":"1.0","pl":"0.0","resettablePL":"0.0","financing":"0.0"},"short":{"units":"0.0","pl":"-0.0005","resettablePL":"-0.0005","financing":"0.0"},"financing":"0.0"}],"transactions":[{"id":"4955","time":"1510528065.059959057","userID":6557245,"accountID":"123-123-1234567-123","batchID":"4955","requestID":"24350012415650903","type":"MARKET_ORDER","reason":"CLIENT_ORDER","orderID":null,"financing":null,"accountBalance":null,"price":null,"instrument":"AUD_JPY","units":"1.0","fullPrice":null,"pl":null,"commission":null,"tradeOpened":null},{"id":"4956","time":"1510528065.059959057","userID":6557245,"accountID":"123-123-1234567-123","batchID":"4955","requestID":"24350012415650903","type":"ORDER_FILL","reason":"MARKET_ORDER","orderID":4955,"financing":"0.0","accountBalance":"97804.9353","price":"86.918","instrument":"AUD_JPY","units":"1.0","fullPrice":{"bids":[{"price":"86.894","liquidity":10000000}],"asks":[{"price":"86.918","liquidity":10000000}],"closeoutBid":"86.894","closeoutAsk":"86.918","timestamp":"1510528058.508284733"},"pl":"0.0","commission":"0.0","tradeOpened":{"tradeID":4956,"units":"1.0"}}]}'

example_trade_summary = {'id': 4991, 'instrument': 'AUD_JPY', 'price': '87.054', 'openTime': '1510549344.465586871',
                         'state': 'OPEN',
                         'initialUnits': '1.0', 'currentUnits': '1.0', 'realizedPL': '0.0', 'averageClosePrice': None,
                         'closingTransactionIDs': None, 'financing': '0.0', 'closeTime': None}

example_changed_trade_summary = {'id': 4991, 'instrument': 'AUD_JPY', 'price': '87.054',
                                 'openTime': '1510549344.465586871', 'state': 'CLOSED', 'initialUnits': '1.0',
                                 'currentUnits': '0.0', 'realizedPL': '-0.0003', 'averageClosePrice': '87.026',
                                 'closingTransactionIDs': ['4995'], 'financing': '0.0',
                                 'closeTime': '1510552170.804347695'}

example_order = {'id': '5053', 'createTime': '1510584559.111762008', 'type': 'STOP',
         'instrument': 'AUD_JPY', 'units': '5', 'timeInForce': 'GTD',
         'price': '86.885', 'gtdTime': '1511189310.000000000',
         'triggerCondition': 'DEFAULT', 'partialFill': 'DEFAULT_FILL',
         'positionFill': 'DEFAULT', 'state': 'PENDING'}
