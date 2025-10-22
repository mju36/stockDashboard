###class that will get the volume of put / call side for each contract & optionChain to get ratio for each option & optionChain. e.g, P/C ratio 0.83
import dataClasses.Ticker as Ticker
import dataClasses.Option as Option
import dataClasses.OptionChain as OptionChain
class analytics:
    def __init__(self, optionchain : OptionChain):
        self.optionchain = optionchain

    def put_call_volume_ratio(self, optionchain): #can make this faster once i am sure that call_chain and put_chain have same strikes
        call_vol = 0
        put_vol = 0

        # Sum call volumes
        for strike, opt in optionchain.get_call_chain().items():
            volume = opt.get_volume() or 0
            call_vol += volume

        # Sum put volumes
        for strike, opt in optionchain.get_put_chain().items():
            volume = opt.get_volume() or 0
            put_vol += volume

        return put_vol / call_vol if call_vol else None

    def strikes_volume_ratio(self, optionchain):
        result = {}
        all_strikes = set(optionchain.get_call_chain().keys()) | set(optionchain.get_put_chain().keys())
        for strike in all_strikes:
            call_option = optionchain.call_chain.get(strike)
            put_option = optionchain.put_chain.get(strike)

            call_vol = (call_option.get_volume() or 0) if call_option else 0
            put_vol = (put_option.get_volume() or 0) if put_option else 0
            ratio = put_vol / call_vol if call_vol else None
            result[strike] = {
                "call_vol": call_vol,
                "put_vol": put_vol,
                "total_vol": call_vol + put_vol,
                "ratio": ratio
            }
        return result

    def gex_per_strike(self, optionchain):
        ###GEXcall​=Gamma×Open Interest×100×0.01
        result = {}
        all_strikes = set(optionchain.get_call_chain().keys()) | set(optionchain.get_put_chain().keys())
        for strike in all_strikes:
            call_option = optionchain.call_chain.get(strike)
            put_option = optionchain.put_chain.get(strike)

            # Handle None values for gamma and open_interest
            if call_option:
                call_gamma = call_option.get_gamma() or 0
                call_oi = call_option.get_open_interest() or 0
                call_gex = call_gamma * call_oi * 100 * 0.01
            else:
                call_gex = 0

            if put_option:
                put_gamma = put_option.get_gamma() or 0
                put_oi = put_option.get_open_interest() or 0
                put_gex = -(put_gamma * put_oi * 100 * 0.01)
            else:
                put_gex = 0

            direction_gex = call_gex + put_gex
            abs_gex = call_gex + abs(put_gex)
            result[strike] = {
                "call_gex": call_gex,
                "put_gex": put_gex,
                "direction_gex": direction_gex,
                "abs_gex": abs_gex
            }
        return result
