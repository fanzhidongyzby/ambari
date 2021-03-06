/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.ambari.server.orm.dao;

import java.text.MessageFormat;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.TypedQuery;

import org.apache.ambari.server.actionmanager.HostRoleStatus;
import org.apache.ambari.server.orm.RequiresSession;
import org.apache.ambari.server.orm.entities.RequestEntity;
import org.apache.ambari.server.orm.entities.RequestResourceFilterEntity;
import org.eclipse.persistence.config.HintValues;
import org.eclipse.persistence.config.QueryHints;

import com.google.inject.Inject;
import com.google.inject.Provider;
import com.google.inject.Singleton;
import com.google.inject.persist.Transactional;

@Singleton
public class RequestDAO {
  /**
   * SQL template to retrieve all request IDs, sorted by the ID.
   */
  private final static String REQUEST_IDS_SORTED_SQL = "SELECT request.requestId FROM RequestEntity request ORDER BY request.requestId {0}";
  private final static String CLUSTER_REQUEST_IDS_SORTED_SQL = "SELECT request.requestId FROM RequestEntity request where request.clusterId=:clusterId ORDER BY request.requestId {0}";

  @Inject
  Provider<EntityManager> entityManagerProvider;

  @Inject
  DaoUtils daoUtils;

  @RequiresSession
  public RequestEntity findByPK(Long requestId) {
    return entityManagerProvider.get().find(RequestEntity.class, requestId);
  }

  public List<RequestEntity> findByPks(Collection<Long> requestIds) {
    return findByPks(requestIds, false);
  }

  /**
   * Given a collection of request ids, load the corresponding entities
   * @param requestIds  the collection of request ids
   * @param refreshHint {@code true} to hint JPA that the list should be refreshed
   * @return the list entities. An empty list if the requestIds are not provided
   */
  @RequiresSession
  public List<RequestEntity> findByPks(Collection<Long> requestIds, boolean refreshHint) {
    if (null == requestIds || 0 == requestIds.size()) {
      return Collections.emptyList();
    }

    TypedQuery<RequestEntity> query = entityManagerProvider.get().createQuery("SELECT request FROM RequestEntity request " +
        "WHERE request.requestId IN ?1", RequestEntity.class);

    // !!! https://bugs.eclipse.org/bugs/show_bug.cgi?id=398067
    // ensure that an associated entity with a JOIN is not stale
    if (refreshHint) {
      query.setHint(QueryHints.REFRESH, HintValues.TRUE);
    }

    return daoUtils.selectList(query, requestIds);
  }

  @RequiresSession
  public List<RequestEntity> findAll() {
    return daoUtils.selectAll(entityManagerProvider.get(), RequestEntity.class);
  }

  @RequiresSession
  public List<Long> findAllRequestIds(int limit, boolean ascending) {
    String sort = "ASC";
    if (!ascending) {
      sort = "DESC";
    }

    String sql = MessageFormat.format(REQUEST_IDS_SORTED_SQL, sort);
    TypedQuery<Long> query = entityManagerProvider.get().createQuery(sql,
        Long.class);

    query.setMaxResults(limit);

    return daoUtils.selectList(query);
  }
  
  @RequiresSession
  public List<Long> findAllRequestIds(long clusterId, int limit, boolean ascending) {
	  String sort = "ASC";
	  if (!ascending) {
		  sort = "DESC";
	  }
	  
	  String sql = MessageFormat.format(CLUSTER_REQUEST_IDS_SORTED_SQL, sort);
	  TypedQuery<Long> query = entityManagerProvider.get().createQuery(sql,
			  Long.class);
	  
	  query.setMaxResults(limit);
	  query.setParameter("clusterId", clusterId);
	  return daoUtils.selectList(query);
  }

  @RequiresSession
  public List<RequestResourceFilterEntity> findAllResourceFilters() {
    return daoUtils.selectAll(entityManagerProvider.get(), RequestResourceFilterEntity.class);
  }

  @RequiresSession
  public boolean isAllTasksCompleted(long requestId) {
    TypedQuery<Long> query = entityManagerProvider.get().createQuery(
        "SELECT task.taskId FROM HostRoleCommandEntity task WHERE task.requestId = ?1 AND " +
          "task.stageId=(select max(stage.stageId) FROM StageEntity stage WHERE stage.requestId=?1) " +
          "AND task.status NOT IN ?2",
        Long.class
    );
    query.setMaxResults(1); //we don't need all
    return daoUtils.selectList(query, requestId, HostRoleStatus.getCompletedStates()).isEmpty();
  }

  @RequiresSession
  public Long getLastStageId(long requestId) {
    TypedQuery<Long> query = entityManagerProvider.get().createQuery("SELECT max(stage.stageId) " +
      "FROM StageEntity stage WHERE stage.requestId=?1", Long.class);
    return daoUtils.selectSingle(query, requestId);
  }

  @Transactional
  public void create(RequestEntity requestEntity) {
    entityManagerProvider.get().persist(requestEntity);
  }

  @Transactional
  public RequestEntity merge(RequestEntity requestEntity) {
    return entityManagerProvider.get().merge(requestEntity);
  }

  @Transactional
  public void remove(RequestEntity requestEntity) {
    entityManagerProvider.get().remove(merge(requestEntity));
  }

  @Transactional
  public void removeByPK(Long requestId) {
    remove(findByPK(requestId));
  }
}
