//  Copyright 2017 Twitter. All rights reserved.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//  http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.

package com.twitter.heron.streamlet.impl.streamlets;

import java.util.Set;

import com.twitter.heron.api.topology.TopologyBuilder;
import com.twitter.heron.streamlet.Source;
import com.twitter.heron.streamlet.impl.StreamletImpl;
import com.twitter.heron.streamlet.impl.sources.ComplexSource;

/**
 * SourceStreamlet is a very quick and flexible way of creating a Streamlet
 * from a user supplied Generator Function. The Generator function is the
 * source of all tuples for this Streamlet.
 */
public class SourceStreamlet<R> extends StreamletImpl<R> {
  private Source<R> generator;

  public SourceStreamlet(Source<R> generator) {
    this.generator = generator;
    setNumPartitions(1);
  }

  @Override
  public boolean doBuild(TopologyBuilder bldr, Set<String> stageNames) {
    setDefaultNameIfNone(StreamletNamePrefixes.SOURCE.toString(), stageNames);
    bldr.setSpout(getName(), new ComplexSource<R>(generator), getNumPartitions());
    return true;
  }
}
