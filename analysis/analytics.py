###class that will get the volume of put / call side for each contract & optionChain to get ratio for each option & optionChain. e.g, P/C ratio 0.83
import dataClasses.Ticker as Ticker
import dataClasses.Option as Option
import dataClasses.OptionChain as OptionChain
class analytics:
    def __init__(self, optionchain : OptionChain):
        optionchain = optionchain

    def put_call_volume_ratio(optionchain): #can make this faster once i am sure that call_chain and put_chain have same strikes
        call_vol = 0
        put_vol = 0
        combined_dict = {**optionchain.get_call_chain,**optionchain.get_put_chain}
        for strike, opt in combined_dict.items():
            if opt.get_option_type == "call":
                call_vol += opt.get_volume()
            else:
                put_vol += opt.get_volume()

        return put_vol / call_vol if call_vol else None
    
    def strikes_volume_ratio(optionchain):
         '''
         for each strike in optionchain, we will get ratio to determine possible inflection points, can return an array holding 3 vals, put vol, call vol, and ratio 
         '''