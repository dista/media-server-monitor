'''
Created on 2011-12-17

@author: dista
'''

from common import parser, time_extra
import copy

class Analyzer:
    def __init__(self):
        pass
    
    def do_analyze(self, sample_time, http_response, exists_samples):
        ret = {"score": 0, "sample": None}

        if http_response.header['code'] != 200:
            ret['sample'] = self._build_failed_sample(sample_time, http_response.header['code_des'])
            return ret

        ret['sample'] = parser.parse_ms_monitor_result(http_response.body)
        ret['sample']['sample_time'] = sample_time

        samples = copy.copy(exists_samples)
        samples.insert(0, ret['sample'])

        ret['score'], ret['score_detail'] = self._cal_score(samples)
        ret['is_failed'] = False
        return ret

    def _build_failed_sample(self, sample_time, http_code_des):
        return {
                'is_failed': True,
                'failed_reason': http_code_des,
                'sample_time': sample_time,
                'total_gops': 0,
                'upstream_opened_count': 0,
                'upstream_connected_count': 0,
                'upstream_connection_fail_count': 0,
                'upstream_bytes_received': 0,
                'clients_connected': 0,
                'total_clients_served': 0,
                'total_bytes_sent': 0,
                'live_delay_ms': 0,
                'average_upstream_kbps': 0,
                'average_downstream_kbps': 0,
                'stream_info_audiodatarate': 0,
                'stream_info_videodatarate': 0,
                'stream_info_audiocodecid': 0,
                'stream_info_audiosamplesize': 0,
                'stream_info_audiosamplerate': 0,
                'stream_info_stereo': 0,
                'stream_info_videocodecid': 0,
                'stream_info_framerate': 0,
                'stream_info_width': 0,
                'stream_info_height': 0
                }

    def _cal_score(self, samples):
        current_sample = samples[0]
        data_rate = current_sample['stream_info_audiodatarate'] + current_sample['stream_info_videodatarate']

        score = 0
        score_detail = {"stream_value": 0, "upstream_value": 0, "downstream_value": 0, "live_delay_value": 0}

        #cal stream score
        if data_rate <= 0:
            score = 0
            return (score, score_detail)

        score_detail['stream_value'] = 100

        #cal upstream score
        current_upstream_kbps = self._get_current_upstream_kbps(samples)
        score_detail['upstream_value'] = int(current_upstream_kbps / data_rate * 100)
        #TODO: delete this
        score_detail['computed_upstream_value'] = score_detail['upstream_value']
        if score_detail['upstream_value'] > 100:
            score_detail['upstream_value'] = 100

        #TODO: there is no reliable way to cal downstream score now, so we just set it to 100
        score_detail['downstream_value'] = 100

        #TODO: live_delay
        score_detail['live_delay_value'] = int((10000 - current_sample["live_delay_ms"]) / float(10000) * 100)

        score = 0.8 * score_detail['upstream_value'] + 0.0 * score_detail['downstream_value'] + 0.2 * score_detail['live_delay_value']

        return (int(score), score_detail)

    def _get_current_upstream_kbps(self, samples):
        current_sample = samples[0]
        compare_sample = self._get_kbps_cal_sample(samples)

        if current_sample == compare_sample:
            return current_sample['average_upstream_kbps']
        else:
            time_past_in_secs = time_extra.total_seconds((current_sample['sample_time'] - compare_sample['sample_time']))

            current_upstream_kbps = (current_sample['upstream_bytes_received'] - compare_sample['upstream_bytes_received']) / float(time_past_in_secs) * 8 / 1000
            return current_upstream_kbps

    def _get_kbps_cal_sample(self, samples):
        index = 0
        for i in xrange(1, len(samples)):
            data_rate = samples[i]['stream_info_audiodatarate'] + samples[i]['stream_info_videodatarate']
            if i > 99 or data_rate <= 0:
                break
            index = i

        return samples[index]
