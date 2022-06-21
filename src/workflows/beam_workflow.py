import os

import apache_beam as beam
from apache_beam.io.textio import ReadFromText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.runners.interactive.interactive_runner import InteractiveRunner
from apache_beam.testing.test_pipeline import TestPipeline

from roi_web import baseParseUrl, baseFetchResponse, baseProcessResponse, basePersistProcessed, basePersistResponse

if __name__ == '__main__':
	base_source = os.environ.get( "GNOSIS_WEB_STREAM", "" )
	opts = PipelineOptions()
	with TestPipeline(  ) as p:
		raw = (p
		       | "Load Data" >> ReadFromText( base_source, skip_header_lines = 1 )
		       | "Parse Url" >> beam.Map( lambda x: baseParseUrl( x ) )
		       | "Fetch Response" >> beam.Map( lambda x: x.flatMap( baseFetchResponse ) )
		       )
		raw | "Persist Raw" >> beam.FlatMap( lambda x: basePersistResponse( x ) )

		(raw
		 | "Process Raw" >> beam.Map( lambda x: x.flatMap( baseProcessResponse ) )
		 | "Persist Processed" >> beam.Map( lambda x: basePersistProcessed( x ) )
		 )